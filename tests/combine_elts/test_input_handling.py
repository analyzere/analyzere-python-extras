import pytest

from analyzere_extras.combine_elts import ELTCombiner
from requests import ConnectionError


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
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_uuid('invaliduuid')

        assert str(value_error.value) == 'badly formed hexadecimal UUID string'

    def test_unknown_valid_uuid(self):
        unknown_uuid = '874f0b1f-b00d-49b3-ab78-c7a626e3addf'

        elt_combiner = ELTCombiner()
        with pytest.raises(ValueError) as value_error:
            elt_combiner._process_uuid(unknown_uuid)

        assert str(value_error.value) == \
            "UUID '874f0b1f-b00d-49b3-ab78-c7a626e3addf' is not " \
            "a Portfolio, PortfolioView, Layer, LayerView, or LossSet."


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
