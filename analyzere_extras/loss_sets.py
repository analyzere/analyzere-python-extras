import hashlib
import csv
from collections import defaultdict

from analyzere import (
    LossSet,
    Distribution,
    Layer,
    LayerView,
    LossFilter
)

# Analogous Event Scenario Loss Set. This class is designed to take a set
# of loss sets and a list of Event IDs and combine them into a single loss
# set for doing realistic disaster scenario type analysis.


class AnalogousEventLossSet(LossSet):

    _collection_name = 'loss_sets'

    def __init__(self,
                 analysis_profile='',
                 load=1.0,
                 source_events=[],
                 sources=[],
                 occurrence_probability=1.0,
                 **kwargs):

        self.analysis_profile = analysis_profile
        self.source_events = source_events
        self.sources = sources
        self.load = load
        self.occurrence_probability = occurrence_probability

        return super(AnalogousEventLossSet, self).__init__(
            type='ParametricLossSet',
            **kwargs
        )

    def _retrieve_loss_data(self):
        loss_data = {}
        for event in self.source_events:
            event_filter = LossFilter(
               type='AnyOfFilter',
               name='Event ' + str(event),
               attribute='EventID',
               values=[event]
            )

            filter_layer = Layer(
                type='FilterLayer',
                description='Event ' + str(event),
                filters=[event_filter],
                loss_sets=self.sources
            )

            yelt = LayerView(
                analysis_profile=self.analysis_profile,
                layer=filter_layer
            ).save().download_yelt(secondary_uncertainty=False)

            yelt_reader = csv.DictReader(yelt.decode('utf-8').splitlines())
            loss_data[event] = [float(row['Loss']) for row in yelt_reader]

        self._loss_data = loss_data

    def _construct_severity_distribution(self):
        self._severity_distr = 'Probability,Loss\n'
        event_probability = 1.0/len(self.source_events)

        value_probabilities = defaultdict(float)
        # Creating the probability for each unique value. This ensures the
        # severity distribution string is as small as possible.
        for event in self.source_events:
            if len(self._loss_data[event]) != 0:
                # Note that a single event id may occur several times in a
                # simulation with different loss values. Each of those values
                # should have the same probability of occuring. The probability
                # of all potential loss values for a single event should add
                # to the probability of the event.
                instance_prob = event_probability/len(self._loss_data[event])
                for loss in self._loss_data[event]:
                    value_probabilities[loss * self.load] += instance_prob
            else:
                value_probabilities[0.0] += event_probability

        # Adding the unique values to severity distribution file that will be
        # uploaded.
        loss_values = sorted(list(value_probabilities.keys()))
        for key in loss_values:
            self._severity_distr += str(value_probabilities[key]) + ',' \
                + str(key) + '\n'

    def _upload_severity_distribution(self):
        data_hash = hashlib.md5(self._severity_distr.encode()).hexdigest()

        severity_description = 'ARe-Python-Extras AnalogousEventLossSetELS ' \
            + 'Generated Resource: ' + data_hash

        distribution_search = Distribution.list(search=severity_description)
        # Check if severity distribution has been created on the server.
        if len(distribution_search) > 0:
            self.severity = distribution_search[0]
        else:
            severity_distr = Distribution(
                type='CustomSeverityDistribution',
                description=severity_description,
            ).save()
            severity_distr.upload_data(self._severity_distr)
            self.severity = severity_distr

    def _upload_frequency_distribution(self):
        freq_description = 'ARe-Python-Extras AnalogousEventLossSetELS ' \
           + 'Generated Resource: Frequency ' \
           + str(self.occurrence_probability)

        distribution_search = Distribution.list(search=freq_description)
        if len(distribution_search) > 0:
            self.frequency = distribution_search[0]
        else:
            freq_distr = Distribution(
                type='BinomialDistribution',
                description=freq_description,
                n=1,
                p=self.occurrence_probability
            ).save()
            self.frequency = freq_distr

    def _upload_seasonality_distribution(self):
        seasonality_description = \
            'ARe-Python-Extras AnalogousEventLossSetELS ' \
            + 'Generated Resource: Seasonality 0.0'

        distribution_search = Distribution.list(search=seasonality_description)
        if len(distribution_search) > 0:
            self.seasonality = distribution_search[0]
        else:
            seasonality_distr = Distribution(
                type='DiracDistribution',
                description=seasonality_description,
                value=0.0,
            ).save()
            self.seasonality = seasonality_distr

    def save(self):
        # Collect keys to retain on the type after saving. Otherwise this
        # information is lost by the super class's save method
        keys_to_retain = ['analysis_profile', 'source_events', 'sources',
                          'load', 'occurrence_probability']
        values_to_retain = {key: self.__dict__[key] for key in keys_to_retain}

        # Adding the above information to loss set's meta_data so that it is
        # retrievable at a later date.
        self.meta_data = {}
        self.meta_data['analysis_profile'] = self.analysis_profile.id
        self.meta_data['source_events'] = \
            ','.join(map(str, self.source_events))
        self.meta_data['sources'] = \
            ','.join([source.id for source in self.sources])
        self.meta_data['load'] = self.load
        self.meta_data['occurrence_probability'] = self.occurrence_probability
        self.meta_data['_type'] = 'AnalogousEventLossSet'

        self._retrieve_loss_data()
        self._construct_severity_distribution()
        self._upload_severity_distribution()
        self._upload_frequency_distribution()
        self._upload_seasonality_distribution()
        super(AnalogousEventLossSet, self).save()

        # Merging the retained values back into the class.
        self.__dict__.update(values_to_retain)
        return self
