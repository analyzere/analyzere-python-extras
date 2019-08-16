import pytest

from analyzere_extras.combine_elts import ELTCombiner
from analyzere import (
    Portfolio,
    PortfolioView,
    Layer,
    LayerView,
    LossSet,
    EventCatalog,
    InvalidRequestError,
)
from requests import ConnectionError
from mock import patch


class AnalyzeReRetrieveAPI():
    """Mocked Analyze Re API to control behaviour of API methods."""

    invalid_request = False

    @classmethod
    def retrieve(self, uuid):
        """Mocked '<Resource>.retrieve()' function."""
        if AnalyzeReRetrieveAPI.invalid_request:
            raise InvalidRequestError
        else:
            raise NotImplementedError

    @classmethod
    def event_catalog_retrieve(self, uuid):
        return None


class TestAddELTLossSets:

    def test_add_portfolio_elts(self, portfolio):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_portfolio_elts(portfolio[2])
        assert len(elt_combiner._elt_loss_sets) == len(portfolio[1])
        for i in range(0, len(portfolio[1])):
            assert elt_combiner._elt_loss_sets[i] == portfolio[1][i]

    def test_add_portfolio_view_with_layer_views_elts(
            self, portfolio_view_with_layer_views):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_portfolio_view_elts(
            portfolio_view_with_layer_views[2])

        assert len(elt_combiner._elt_loss_sets) == len(
            portfolio_view_with_layer_views[1])

        for i in range(0, len(portfolio_view_with_layer_views[1])):
            assert elt_combiner._elt_loss_sets[i] == \
                portfolio_view_with_layer_views[1][i]

    def test_add_portfolio_view_with_portfolio_elts(
            self, portfolio_view_with_portfolio):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_portfolio_view_elts(
            portfolio_view_with_portfolio[2])

        assert len(elt_combiner._elt_loss_sets) == len(
            portfolio_view_with_portfolio[1])

        for i in range(0, len(portfolio_view_with_portfolio[1])):
            assert elt_combiner._elt_loss_sets[i] == \
                portfolio_view_with_portfolio[1][i]

    def test_add_layer_elts(self, layer):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_layer_elts(layer[2])
        assert len(elt_combiner._elt_loss_sets) == len(layer[1])
        for i in range(0, len(layer[1])):
            assert elt_combiner._elt_loss_sets[i] == layer[1][i]

    def test_add_layer_view_elts(self, layer_view):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_layer_view_elts(layer_view[2])
        assert len(elt_combiner._elt_loss_sets) == len(layer_view[1])
        for i in range(0, len(layer_view[1])):
            assert elt_combiner._elt_loss_sets[i] == layer_view[1][i]

    def test_add_loss_set_elt(self, loss_set):
        elt_combiner = ELTCombiner()
        assert len(elt_combiner._elt_loss_sets) == 0

        elt_combiner._add_loss_set_elt(loss_set[1])
        assert len(elt_combiner._elt_loss_sets) == 1
        assert elt_combiner._elt_loss_sets[0] == loss_set[0]

    def test_non_elt_warning_add_portfolio_elts(
            self, portfolio_with_non_elt_loss_sets):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_portfolio_elts(
                portfolio_with_non_elt_loss_sets[2])

        assert len(warnings) == len(portfolio_with_non_elt_loss_sets[1])
        for i in range(0, len(warnings)):
            assert str(warnings[i].message.args[0]) == (
                'Portfolio {} contains non-ELT LossSet {}. Non-ELT LossSets '
                'are ignored.'.format(
                    portfolio_with_non_elt_loss_sets[0],
                    portfolio_with_non_elt_loss_sets[1][i]))

    def test_non_elt_warning_add_pv_with_p_elts(
            self, pv_with_p_with_non_elt_loss_sets):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_portfolio_view_elts(
                pv_with_p_with_non_elt_loss_sets[2])

        assert len(warnings) == len(pv_with_p_with_non_elt_loss_sets[1])
        for i in range(0, len(warnings)):
            assert str(warnings[i].message.args[0]) == (
                'PortfolioView {} contains non-ELT LossSet {}. Non-ELT '
                'LossSets are ignored.'.format(
                    pv_with_p_with_non_elt_loss_sets[0],
                    pv_with_p_with_non_elt_loss_sets[1][i]))

    def test_non_elt_warning_add_pv_with_lv_elts(
            self, pv_with_lv_with_non_elt_loss_sets):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_portfolio_view_elts(
                pv_with_lv_with_non_elt_loss_sets[2])

        assert len(warnings) == len(pv_with_lv_with_non_elt_loss_sets[1])
        for i in range(0, len(warnings)):
            assert str(warnings[i].message.args[0]) == (
                'PortfolioView {} contains non-ELT LossSet {}. Non-ELT '
                'LossSets are ignored.'.format(
                    pv_with_lv_with_non_elt_loss_sets[0],
                    pv_with_lv_with_non_elt_loss_sets[1][i]))

    def test_non_elt_warning_add_layer_elts(
            self, layer_with_non_elt_loss_sets):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_layer_elts(layer_with_non_elt_loss_sets[2])

        assert len(warnings) == len(layer_with_non_elt_loss_sets[1])
        for i in range(0, len(warnings)):
            assert str(warnings[i].message.args[0]) == (
                'Layer {} contains non-ELT LossSet {}. Non-ELT LossSets are '
                'ignored.'.format(
                    layer_with_non_elt_loss_sets[0],
                    layer_with_non_elt_loss_sets[1][i]))

    def test_non_elt_warning_add_layer_view_elts(
            self, layer_view_with_non_elt_loss_sets):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_layer_view_elts(
                layer_view_with_non_elt_loss_sets[2])

        assert len(warnings) == len(layer_view_with_non_elt_loss_sets[1])
        for i in range(0, len(warnings)):
            assert str(warnings[i].message.args[0]) == (
                'LayerView {} contains non-ELT LossSet {}. Non-ELT LossSets '
                'are ignored.'.format(
                    layer_view_with_non_elt_loss_sets[0],
                    layer_view_with_non_elt_loss_sets[1][i]))

    def test_non_elt_warning_add_loss_set_elt(self, non_elt_loss_set):
        elt_combiner = ELTCombiner()

        with pytest.warns(UserWarning) as warnings:
            elt_combiner._add_loss_set_elt(non_elt_loss_set[1])

        assert len(warnings) == 1
        assert str(warnings[0].message.args[0]) == (
            'LossSet {} is not an ELT LossSet. Non-ELT LossSets '
            'are ignored.'.format(non_elt_loss_set[0]))


class TestProcessUUID:

    def test_invalid_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    def test_invalid_portfolio_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_portfolio_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    def test_invalid_portfolio_view_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_portfolio_view_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    def test_invalid_layer_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_layer_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    def test_invalid_layer_view_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_layer_view_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    def test_invalid_loss_set_uuid(self):
        elt_combiner = ELTCombiner()

        invalid_uuid = 'invaliduuid'
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_loss_set_uuid(invalid_uuid)

        assert str(value_error.value) == "'{}' is not a valid UUID.".format(
            invalid_uuid)

    @patch.object(Portfolio, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(PortfolioView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(Layer, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(LayerView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(LossSet, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a Portfolio, PortfolioView, Layer, LayerView, or LossSet."

    @patch.object(Portfolio, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_portfolio_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_portfolio_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a Portfolio."

    @patch.object(PortfolioView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_portfolio_view_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_portfolio_view_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a PortfolioView."

    @patch.object(Layer, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_layer_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_layer_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a Layer."

    @patch.object(LayerView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_layer_view_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_layer_view_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a LayerView."

    @patch.object(LossSet, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    def test_unknown_valid_loss_set_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        AnalyzeReRetrieveAPI.invalid_request = True

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_loss_set_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a LossSet."

    @patch.object(Portfolio, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(PortfolioView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(Layer, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(LayerView, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(LossSet, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(
        EventCatalog, 'retrieve', AnalyzeReRetrieveAPI.event_catalog_retrieve)
    @pytest.mark.parametrize(
        'resource_type',
        ['Portfolio', 'PortfolioView', 'Layer', 'LayerView', 'LossSet', 'all'])
    def test_multiple_valid_unknown_uuids(self, resource_type):

        AnalyzeReRetrieveAPI.invalid_request = True

        uuid_1 = 'd4678873-85fa-42f3-aae6-7f9cd541a66a'
        uuid_2 = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'
        uuid_3 = '279c6c55-94fe-4738-8d34-f0cf4d92e759'

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner.combine_elts_from_resources(
                [uuid_1, uuid_2, uuid_3],
                'fake catalog',
                uuid_type=resource_type
            )

        error_message_resource_str = resource_type
        if error_message_resource_str == 'all':
            error_message_resource_str = ('Portfolio, PortfolioView, Layer, '
                                          'LayerView, or LossSet')

        expected_message = "UUID '{}' is not a {}."
        expected_messages = []
        for uuid in [uuid_1, uuid_2, uuid_3]:
            expected_messages.append(expected_message.format(
                uuid, error_message_resource_str))

        assert str(value_error.value) == '\n'.join(expected_messages)

    @patch.object(LossSet, 'retrieve', AnalyzeReRetrieveAPI.retrieve)
    @patch.object(
        EventCatalog, 'retrieve', AnalyzeReRetrieveAPI.event_catalog_retrieve)
    def test_multiple_invalid_uuids(self):

        AnalyzeReRetrieveAPI.invalid_request = True

        uuid_1 = 'invalid1'
        uuid_2 = 'st1ll_n0t_v4l1d'
        uuid_3 = 'wrong again'

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner.combine_elts_from_resources(
                [uuid_1, uuid_2, uuid_3],
                'fake catalog',
                uuid_type='LossSet'
            )

        expected_message = "'{}' is not a valid UUID."
        expected_messages = []
        for uuid in [uuid_1, uuid_2, uuid_3]:
            expected_messages.append(expected_message.format(uuid))

        assert str(value_error.value) == '\n'.join(expected_messages)


class TestConnectionError:

    def test_connection_error_thrown(self):
        """Requests by Id don't work unless you have defined the following
        analyzere varialbes, and a connecton can be established
           - analyzere.base_url
           - analyzere.username
           - analyzere.password
        """
        uuid = 'd4678873-85fa-42f3-aae6-7f9cd541a66a'
        catalog_id = '279c6c55-94fe-4738-8d34-f0cf4d92e759'
        elt_combiner = ELTCombiner()

        with pytest.raises(ConnectionError):
            elt_combiner.combine_elts_from_resources(
                [uuid],
                catalog_id)
