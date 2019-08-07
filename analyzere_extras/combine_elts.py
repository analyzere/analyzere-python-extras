from __future__ import print_function
import analyzere
import multiprocessing
import ssl
import certifi
import csv

from uuid import UUID
from analyzere import (
    Portfolio,
    Layer,
    LayerView,
    LossSet,
    EventCatalog
)

from six.moves import urllib
from concurrent.futures import ThreadPoolExecutor


class ELTCombiner():
    """Functionality for combining multiple ELTs into one ELT.

    Assumes the following have been set:
        analyzere.base_url
        analyzere.username
        analyzere.password
    """

    def __init__(self):
        self._elt_loss_sets = []
        self._downloaded_elts = {}

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())
        httpsHandler = urllib.request.HTTPSHandler(context=context)

        manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        manager.add_password(None, analyzere.base_url,
                             analyzere.username, analyzere.password)
        authHandler = urllib.request.HTTPBasicAuthHandler(manager)

        opener = urllib.request.build_opener(httpsHandler, authHandler)

        urllib.request.install_opener(opener)

        self._urllib_request = urllib.request

    def combine_elts_from_resources(
            self, uuid_list, catalog_id,
            description='analyzere-python-extras: Combined ELT'):
        """Combine ELTs from multiple resources into one ELT.

        Parameters:

           uuid_list    A list of Portfolio, Layer, LayerView, and/or LossSet
                        UUIDs. The ELTs for these resources will be downloaded,
                        combined into a single ELT, and re-uploaded.
                        Any non-ELT LossSets found will be ignored.

           catalog_id   The UUID of the EventCatalog that corresponds to the
                        resources in uuid_list

           description  A description to be used for the combined loss set.
        """
        self._elt_loss_sets = []
        self._description = description
        self._catalog = EventCatalog.retrieve(catalog_id)

        for uuid in uuid_list:
            self._process_uuid(uuid)

        return self._combine_elts()

    def _process_uuid(self, uuid):
        """Validates uuid as a UUID, and adds ELTs for that UUID to
        self._elt_loss_sets

        Accepts Portfolio, Layer, LayerView, and LossSet UUIDs.
        """
        # Validate UUID - if invalid, let error bubble up
        valid_uuid = UUID(uuid, version=4)

        portfolio = None
        layer = None
        layer_view = None
        loss_set = None

        try:
            portfolio = Portfolio.retrieve(valid_uuid)
        except:
            try:
                layer = Layer.retrieve(valid_uuid)
            except:
                try:
                    layer_view = LayerView.retrieve(valid_uuid)
                except:
                    try:
                        loss_set = LossSet.retrieve(valid_uuid)
                    except:
                        print('Error: UUID {} is not a Portfolio, Layer, '
                              'LayerView, or LossSet.'.format(valid_uuid))

        if portfolio is not None:
            self._add_portfolio_elts(portfolio)

        elif layer is not None:
            self._add_layer_elts(layer)

        elif layer_view is not None:
            self._add_layer_view_elts(layer_view)

        elif loss_set is not None:
            self._add_loss_set_elt(loss_set)

    def _combine_elts(self):
        """Downloads the ELTs in self._elt_loss_sets (a list of ELTLossSet ids)
        and uploads a singe combined ELT.
        """
        downloaded = 0
        with ThreadPoolExecutor(multiprocessing.cpu_count()) as executor:
            for loss_set in executor.map(self._download_loss_set,
                                         self._elt_loss_sets):
                downloaded += 1
                print('\rELTLossSets downloaded: {}'.format(downloaded),
                      end='')

        print('\n')
        return self._upload_combined_elt()

    def _download_loss_set(self, loss_set_id):
        """Downloads loss_set_id's ELT
        """
        loss_set = LossSet.retrieve(loss_set_id)
        loss_set_filename = loss_set.data.name
        elt_url = '{}/uploads/files/{}'.format(analyzere.base_url,
                                               loss_set_filename)

        elt_response = self._urllib_request.urlopen(elt_url)

        self._downloaded_elts[loss_set_id] = elt_response

    def _upload_combined_elt(self):
        # Append loss sets
        combined_elt_data = ["EventId,Loss,STDDEVI,STDDEVC,EXPVALUE"]

        for elt_id, elt_response in self._downloaded_elts.items():
            reader = csv.DictReader(elt_response.read().decode(
                'utf-8').splitlines())

            event_column = 'EventId'
            if 'EventId' not in reader.fieldnames:
                event_column = 'EventID'

            for row in reader:
                eventid = row[event_column]
                loss = row['Loss']
                stdevi = row.get('STDDEVI', '0.0')
                stdevc = row.get('STDDEVC', '0.0')
                expval = row.get('EXPVALUE', loss)
                combined_elt_data.append(','.join([
                    eventid, loss, stdevi, stdevc, expval]))

        combined_elt_data = '\n'.join(combined_elt_data)

        # Upload as new loss set
        combined_loss_set = LossSet(
            type='ELTLossSet',
            description=self._description,
            loss_type='LossGross',
            currency='USD',
            event_catalogs=[self._catalog]
        )

        combined_loss_set = combined_loss_set.save()
        combined_loss_set.upload_data(combined_elt_data)
        print('Combined ELT LossSet Id: {}'.format(combined_loss_set.id))
        return combined_loss_set

    def _add_portfolio_elts(self, portfolio):
        """Adds ELTs from layers in portfolio to self._elt_loss_sets.
        """
        for layer in portfolio.layers:
            for loss_set in layer.loss_sets:
                if loss_set.type == 'ELTLossSet':
                    self._elt_loss_sets.append(loss_set.id)
                else:
                    print('Warning: Portfolio {} contains non-ELT LossSet {}. '
                          'Non-ELT LossSets are ignored.'.format(
                              portfolio.id, loss_set.id))

    def _add_layer_elts(self, layer):
        """Adds ELTs from layer to self._elt_loss_sets.
        """
        for loss_set in layer.loss_sets:
            if loss_set.type == 'ELTLossSet':
                self._elt_loss_sets.append(loss_set.id)
            else:
                print('Warning: Layer {} contains non-ELT LossSet {}. '
                      'Non-ELT LossSets are ignored.'.format(
                          layer.id, loss_set.id))

    def _add_layer_view_elts(self, layer_view):
        """Adds ELTs from layer in layer_view to self._elt_loss_sets.
        """
        for loss_set in layer_view.layer.loss_sets:
            if loss_set.type == 'ELTLossSet':
                self._elt_loss_sets.append(loss_set.id)
            else:
                print('Warning: LayerView {} contains non-ELT LossSet {}. '
                      'Non-ELT LossSets are ignored.'.format(layer_view.id,
                                                             loss_set.id))

    def _add_loss_set_elt(self, loss_set):
        """Adds loss_set elt to self._elt_loss_sets.
        """
        if loss_set.type == 'ELTLossSet':
            self._elt_loss_sets.append(loss_set.id)
        else:
            print('Warning: LossSet {} is not an ELT LossSet. '
                  'Non-ELT LossSets are ignored.'.format(loss_set.id))
