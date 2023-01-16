from __future__ import print_function
import analyzere
import multiprocessing
import ssl
import csv
import warnings
import certifi

from six.moves.http_client import IncompleteRead
from uuid import UUID
from analyzere import (
    Portfolio,
    PortfolioView,
    Layer,
    LayerView,
    LossSet,
    EventCatalog,
    InvalidRequestError,
)

from six.moves import urllib
from concurrent.futures import ThreadPoolExecutor
warnings.simplefilter('always', UserWarning)


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
            uuid_type='all',
            description='analyzere-python-extras: Combined ELT'):
        """Combine ELTs from multiple resources into one ELT.

        Parameters:

           uuid_list    A list of Portfolio, Layer, LayerView, and/or LossSet
                        UUIDs. The ELTs for these resources will be downloaded,
                        combined into a single ELT, and re-uploaded.
                        Any non-ELT LossSets found will be ignored.

           catalog_id   The UUID of the EventCatalog that corresponds to the
                        resources in uuid_list.

           uuid_type    Specifies what types of uuids are provided in
                        uuid_list.
                        Valid options:
                        - all
                        - Layer
                        - LayerView
                        - Portfolio
                        - PortfolioView
                        - LossSet

           description  A description to be used for the combined loss set.
        """
        self._elt_loss_sets = []
        self._description = description

        self._catalog = EventCatalog.retrieve(catalog_id)

        # remove any empty strings (if someone had as extra comma)
        uuid_list = [uuid for uuid in uuid_list if uuid is not '']

        errors = []

        if uuid_type == 'Layer':
            for uuid in uuid_list:
                try:
                    self._process_layer_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        elif uuid_type == 'LayerView':
            for uuid in uuid_list:
                try:
                    self._process_layer_view_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        elif uuid_type == 'Portfolio':
            for uuid in uuid_list:
                try:
                    self._process_portfolio_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        elif uuid_type == 'PortfolioView':
            for uuid in uuid_list:
                try:
                    self._process_portfolio_view_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        elif uuid_type == 'LossSet':
            for uuid in uuid_list:
                try:
                    self._process_loss_set_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        else:
            for uuid in uuid_list:
                try:
                    self._process_uuid(uuid)
                except ValueError as e:
                    errors.append(e)

        if len(errors) > 0:
            raise ValueError('\n'.join([str(error) for error in errors]))

        return self._combine_elts()

    def _validate_uuid(self, uuid):
        try:
            UUID(uuid, version=4)
        except ValueError:
            raise ValueError("'{}' is not a valid UUID.".format(uuid))

    def _process_layer_uuid(self, uuid):
        """Validates uuid as a Layer UUID, and adds ELTs for that UUID to
        self._elt_loss_sets
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        layer = None

        try:
            layer = Layer.retrieve(uuid)
        except InvalidRequestError:
            raise ValueError(
                "UUID '{}' is not a Layer.".format(uuid))

        self._add_layer_elts(layer)

    def _process_layer_view_uuid(self, uuid):
        """Validates uuid as a LayerView UUID, and adds ELTs for that UUID to
        self._elt_loss_sets
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        layer_view = None

        try:
            layer_view = LayerView.retrieve(uuid)
        except InvalidRequestError:
            raise ValueError(
                "UUID '{}' is not a LayerView.".format(uuid))

        self._add_layer_view_elts(layer_view)

    def _process_portfolio_uuid(self, uuid):
        """Validates uuid as a Portfolio UUID, and adds ELTs for that UUID to
        self._elt_loss_sets
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        portfolio = None

        try:
            portfolio = Portfolio.retrieve(uuid)
        except InvalidRequestError:
            raise ValueError(
                "UUID '{}' is not a Portfolio.".format(uuid))

        self._add_portfolio_elts(portfolio)

    def _process_portfolio_view_uuid(self, uuid):
        """Validates uuid as a PortfolioView UUID, and adds ELTs for that UUID to
        self._elt_loss_sets
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        portfolio_view = None

        try:
            portfolio_view = PortfolioView.retrieve(uuid)
        except InvalidRequestError:
            raise ValueError(
                "UUID '{}' is not a PortfolioView.".format(uuid))

        self._add_portfolio_view_elts(portfolio_view)

    def _process_loss_set_uuid(self, uuid):
        """Validates uuid as a LossSet UUID, and adds ELTs for that UUID to
        self._elt_loss_sets
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        loss_set = None

        try:
            loss_set = LossSet.retrieve(uuid)
        except InvalidRequestError:
            raise ValueError(
                "UUID '{}' is not a LossSet.".format(uuid))

        self._add_loss_set_elts(loss_set)

    def _process_uuid(self, uuid):
        """Validates uuid as a UUID, and adds ELTs for that UUID to
        self._elt_loss_sets

        Accepts Portfolio, PortfolioView, Layer, LayerView, and LossSet UUIDs.
        """
        # Validate UUID - if invalid, let error bubble up
        self._validate_uuid(uuid)

        portfolio = None
        portfolio_view = None
        layer = None
        layer_view = None
        loss_set = None

        try:
            portfolio = Portfolio.retrieve(uuid)
        except InvalidRequestError:
            try:
                layer = Layer.retrieve(uuid)
            except InvalidRequestError:
                try:
                    loss_set = LossSet.retrieve(uuid)
                except InvalidRequestError:
                    try:
                        portfolio_view = PortfolioView.retrieve(uuid)
                    except InvalidRequestError:
                        try:
                            layer_view = LayerView.retrieve(uuid)
                        except InvalidRequestError:
                            raise ValueError(
                                "UUID '{}' is not a Portfolio, PortfolioView, "
                                "Layer, LayerView, or LossSet.".format(
                                    uuid))

        if portfolio is not None:
            self._add_portfolio_elts(portfolio)

        elif layer is not None:
            self._add_layer_elts(layer)

        elif loss_set is not None:
            self._add_loss_set_elt(loss_set)

        elif portfolio_view is not None:
            self._add_portfolio_view_elts(portfolio_view)

        elif layer_view is not None:
            self._add_layer_view_elts(layer_view)

    def _combine_elts(self):
        """Downloads the ELTs in self._elt_loss_sets (a list of ELTLossSet ids)
        and uploads a single combined ELT.
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

        elt_response_str_list = None
        max_attempts = 3
        for _ in range(0, max_attempts):
            try:
                elt_response_str_list = self._urllib_request.urlopen(
                    elt_url).read().decode('utf-8').splitlines()
            except IncompleteRead:
                continue

        if elt_response_str_list is None:
            msg = '{} IncompleteRead errors received for LossSet {}'.format(
                max_attempts, loss_set_id)
            raise RuntimeError(msg)

        self._downloaded_elts[loss_set_id] = elt_response_str_list

    def _upload_combined_elt(self):
        # Append loss sets
        combined_elt_data = ["EventId,Loss,STDDEVI,STDDEVC,EXPVALUE"]

        for elt_id, elt_response_str_list in self._downloaded_elts.items():
            reader = csv.DictReader(elt_response_str_list)

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
        combined_elt_data += '\n'

        # Upload as new loss set
        combined_loss_set = LossSet(
            type='ELTLossSet',
            description=self._description,
            loss_type='LossGross',
            currency='USD',
            event_catalogs=[self._catalog]
        ).save()

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
                    warnings.warn('Portfolio {} contains non-ELT LossSet {}. '
                                  'Non-ELT LossSets are ignored.'.format(
                                      portfolio.id, loss_set.id))

    def _add_portfolio_view_elts(self, portfolio_view):
        """Adds ELTs from layers in portfolio view to self._elt_loss_sets.
        """
        if hasattr(portfolio_view, 'portfolio') and \
                portfolio_view.portfolio is not None:
            for layer in portfolio_view.portfolio.layers:
                for loss_set in layer.loss_sets:
                    if loss_set.type == 'ELTLossSet':
                        self._elt_loss_sets.append(loss_set.id)
                    else:
                        warnings.warn(
                            'PortfolioView {} contains non-ELT LossSet '
                            '{}. Non-ELT LossSets are ignored.'.format(
                                  portfolio_view.id, loss_set.id))

        if hasattr(portfolio_view, 'layer_views') and \
                portfolio_view.layer_views is not None:
            for layer_view in portfolio_view.layer_views:
                for loss_set in layer_view.layer.loss_sets:
                    if loss_set.type == 'ELTLossSet':
                        self._elt_loss_sets.append(loss_set.id)
                    else:
                        warnings.warn(
                            'PortfolioView {} contains non-ELT LossSet '
                            '{}. Non-ELT LossSets are ignored.'.format(
                                  portfolio_view.id, loss_set.id))

    def _add_layer_elts(self, layer):
        """Adds ELTs from layer to self._elt_loss_sets.
        """
        for loss_set in layer.loss_sets:
            if loss_set.type == 'ELTLossSet':
                self._elt_loss_sets.append(loss_set.id)
            else:
                warnings.warn('Layer {} contains non-ELT LossSet {}. '
                              'Non-ELT LossSets are ignored.'.format(
                                  layer.id, loss_set.id))

    def _add_layer_view_elts(self, layer_view):
        """Adds ELTs from layer in layer_view to self._elt_loss_sets.
        """
        for loss_set in layer_view.layer.loss_sets:
            if loss_set.type == 'ELTLossSet':
                self._elt_loss_sets.append(loss_set.id)
            else:
                warnings.warn(
                    'LayerView {} contains non-ELT LossSet {}. '
                    'Non-ELT LossSets are ignored.'.format(
                        layer_view.id, loss_set.id))

    def _add_loss_set_elt(self, loss_set):
        """Adds loss_set elt to self._elt_loss_sets.
        """
        if loss_set.type == 'ELTLossSet':
            self._elt_loss_sets.append(loss_set.id)
        else:
            warnings.warn(
                'LossSet {} is not an ELT LossSet. '
                'Non-ELT LossSets are ignored.'.format(loss_set.id))
