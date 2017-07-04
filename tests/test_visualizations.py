import pytest
import uuid

from analyzere.base_resources import convert_to_analyzere_object, Resource
from analyzere import LayerView
from analyzere_extras import visualizations
from datetime import datetime
from requests import ConnectionError
from sys import float_info
from mock import Mock


@pytest.fixture(scope='session')
def layer_view():
    content = {
        'analysis_profile': {
            'ref_id': '4e5bccc9-3ad3-4231-8205-1120c4180daf'
        },
        'id': str(uuid.uuid4()),
        'layer': {
          '_type': 'CatXL',
          'description': '9x12.4 CatXL',
          'attachment': {
            'currency': 'USD',
            'value': 12400000000.0,
          },
          'franchise': {
            'currency': 'USD',
            'value': 0.0,
          },
          'limit': {
            'currency': 'USD',
            'value': 9000000000.0,
            },
          'loss_sets': [
            {
              '_type': 'YELTLossSet',
              'created': '2017-01-17T01:01:01.966052+00:00',
              'currency': 'USD',
              'data': {
                'ref_id': '389e169e-d671-49e5-91ae-3c4a8ed1fcad'
              },
              'data_type': 'csv',
              'description': 'Illinois US ST RES',
              'event_catalogs': [
                {
                  'ref_id': 'c508b867-6d6b-4eaf-aad5-294c4debf6de'
                }
              ],
              'id': 'e60a747e-0556-41ce-9ab9-2102f629f559',
              'loss_type': 'LossGross',
              'modified': '2017-01-17T01:01:16.237408+00:00',
              'profile': {
                'attributes': {
                  'Country': ['US'],
                  'Peril': ['ST'],
                  'Region': ['North America'],
                  'SubRegion': ['AB', 'WY']
                  },
                'avg_annual_loss': 555259274.678332,
                'currency': 'USD',
                'max_loss': 19909099444.0,
                'min_loss': 0.0,
                'non_zero_losses': 133674,
                'num_losses': 133700
                },
              'start_date': '2017-01-01T00:00:00+00:00',
              'status': 'processing_succeeded',
              'trial_count': 10000
            },
            {
              '_type': 'YELTLossSet',
              'created': '2017-01-17T00:20:08.805598+00:00',
              'currency': 'USD',
              'data': {
                'ref_id': 'c28046b7-5a5d-43a9-9324-7327bbd934de'
              },
              'data_type': 'csv',
              'description': 'Nova Scotia Canada EQ COM',
              'event_catalogs': [
                {
                   'ref_id': 'c508b867-6d6b-4eaf-aad5-294c4debf6de'
                }
              ],
              'id': '8bfc42b8-75ed-450a-b474-4f936b449dc3',
              'loss_type': 'LossGross',
              'modified': '2017-01-17T00:20:18.231491+00:00',
              'profile': {
                'attributes': {
                  'Country': ['Canada'],
                  'Peril': ['EQ'],
                  'Region': ['North America'],
                  'SubRegion': ['NB', 'NS', 'PE']
                },
                'avg_annual_loss': 5591.573225,
                'currency': 'USD',
                'max_loss': 51649446.69,
                'min_loss': 4.66,
                'non_zero_losses': 24,
                'num_losses': 24
              },
              'start_date': '2017-01-01T00:00:00+00:00',
              'status': 'processing_succeeded',
              'trial_count': 10000
            }
          ],
          'meta_data': {},
          'nth': 1,
          'participation': 1.0,
          'reinstatements': [
            {
              'brokerage': 0.1,
              'premium': 1.0
              }
          ]
        }
    }
    return convert_to_analyzere_object(content, LayerView)


@pytest.fixture(scope='session')
def layer_view_attachment_warning():
    """Unlimited attachments are warnings"""
    content = {
        'id': str(uuid.uuid4()),
        '_type': 'CatXL',
        'attachment': {
            'currency': 'USD',
            'value': float_info.max,
        }
    }
    return convert_to_analyzere_object(content, LayerView)


@pytest.fixture(scope='session')
def layer_view_participation_warning():
    """No participation is a warning"""
    content = {
        '_type': 'CatXL',
        'participation': 0.0
    }
    return convert_to_analyzere_object(content, LayerView)


@pytest.fixture(scope='session')
def layer_view_filter_warning():
    """A FilterLayer with no filters and invert = false is a warning"""
    content = {
        '_type': 'FilterLayer',
        'filters': [],
        'invert': False
    }
    return convert_to_analyzere_object(content, LayerView)


@pytest.fixture(scope='session')
def layer_view_with_all_terms():
    """A LayerView with all of the possible terms defined.  This is
    intended solely to ensure the terms are emitted in the expected
    order.  The terms below are intentionally listed in reverse display
    order.
    """
    content = {
        '_type': 'EvertyingLayer',
        'premium': {
            'currency': 'USD',
            'value': 21.0,
        },
        'payout_amount': {
            'currency': 'USD',
            'value': 20.0,
        },
        'payout_date': datetime(2018, 12, 19),
        'trigger': {
            'currency': 'USD',
            'value': 18.0,
        },
        'number_of_lines': 17,
        'retained_line': {
            'currency': 'USD',
            'value': 16.0,
        },
        'sums_insured': {
            'currency': 'USD',
            'value': 15.0,
        },
        'aggregate_reset': 14,
        'aggregate_period': 13,
        'aggregate_limit': {
            'currency': 'USD',
            'value': 12.0,
        },
        'aggregate_attachment': {
            'currency': 'USD',
            'value': 11.0,
        },
        'franchise': {
            'value': 10.0,
            'currency': 'USD'
        },
        'event_limit': {
            'currency': 'USD',
            'value': 9.0,
        },
        'reinstatements': [
            {
              'premium': 0.8,
              'brokerage': 0.07
            }],
        'nth': 6,
        'limit': {
            'currency': 'USD',
            'value': 5.0,
        },
        'attachment': {
            'currency': 'USD',
            'value': 4.0,
        },
        'invert': False,
        'filters': [{'name': 'One'}],
        'participation': 0.3,
        'expiry_date': datetime(2018, 2, 2),
        'inception_date': datetime(2017, 1, 1),
        'description': 'All Terms Layer'
        }
    return convert_to_analyzere_object(content, LayerView)


class TestDescriptionFormatter:
    def test_description_with_colon(self):
        raw = 'auto: FilterLayer USHU'
        expected = 'auto: FilterLayer USHU'
        assert visualizations._format_description(raw) == expected

    def test_description_with_windows_file_path(self):
        raw = r'Layer 2 : Z:\losses\alpha.csv'
        expected = r'Layer 2 : Z:\\losses\\alpha.csv'
        actual = visualizations._format_description(raw)
        assert (actual == expected)

    def test_description_with_single_quotes_and_colon(self):
        raw = ("Layer 'auto: Filter by HU' loaded by 1.25")
        expected = 'Layer auto: Filter by HU loaded by 1.25'
        assert visualizations._format_description(raw) == expected


class TestDateFieldFormatter:
    def test_format_DateField(self):
        expected = '2015-06-01'
        date = datetime(2015, 6, 1, 12, 11, 10)
        assert (visualizations._format_DateField(date) == expected)


class TestMoneyFieldFormatter:
    def test_small_MoneyField(self):
        m = {'currency': 'USD', 'value': 123.11}
        mf = convert_to_analyzere_object(m)
        expected = '123 USD'
        assert visualizations._format_MoneyField(mf) == expected

    def test_large_MoneyField(self):
        m = {'currency': 'USD', 'value': 123456789.11}
        mf = convert_to_analyzere_object(m)
        expected = '123,456,789 USD'
        assert visualizations._format_MoneyField(mf) == expected

    def test_unlimited_MoneyField(self):
        m = {'currency': 'USD', 'value': float_info.max}
        mf = convert_to_analyzere_object(m)
        expected = 'unlimited'
        assert visualizations._format_MoneyField(mf) == expected


class TestFiltersFormatter:
    def test_no_filters(self):
        content = {'filters': []}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=(empty)'
        assert warning is False

    def test_max_printable_filters(self):
        content = {'filters': [{'name': 'One'},
                               {'name': 'Two'},
                               {'name': 'Three'}]}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=[\'One\', \'Two\', \'Three\']'
        assert warning is False

    def test_many_filters(self):
        content = {'filters': [{'name': 'One'},
                               {'name': 'Two'},
                               {'name': 'Three'},
                               {'name': 'Four'},
                               {'name': 'Five'}]}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=(5 filters)'
        assert warning is False


class TestReinstatementFormatter:
    def test_no_reinstatements(self):
        content = {'reinstatements': []}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == ''
        assert warning is False

    def test_max_max_printable_reinstatements(self):
        content = {'reinstatements': [{'brokerage': 0.01, 'premium': 0.1},
                                      {'brokerage': 0.02, 'premium': 0.2},
                                      {'brokerage': 0.03, 'premium': 0.3},
                                      {'brokerage': 0.04, 'premium': 0.4}]
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nreinsts=[0.1/0.01, 0.2/0.02, 0.3/0.03, 0.4/0.04]'
        assert warning is False

    def test_many_many_reinstatements(self):
        content = {'reinstatements': [{'brokerage': 0.01, 'premium': 0.1},
                                      {'brokerage': 0.02, 'premium': 0.2},
                                      {'brokerage': 0.03, 'premium': 0.3},
                                      {'brokerage': 0.04, 'premium': 0.4},
                                      {'brokerage': 0.05, 'premium': 0.5}]
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nreinsts=5'
        assert warning is False


class TestCoverageFormatter:
    def test_inception_only(self):
        content = {'inception_date': datetime(2017, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[2017-01-01, inf]'
        assert warning is False

    def test_expiry_only(self):
        content = {'expiry_date': datetime(2018, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[-inf, 2018-01-01]'
        assert warning is False

    def test_inception_and_expiry(self):
        content = {'inception_date': datetime(2017, 1, 1),
                   'expiry_date': datetime(2018, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[2017-01-01, 2018-01-01]'
        assert warning is False


class TestLayerTermsFormatter:
    def test_layer(self, layer_view):
        expected_terms = ('\nshare=100.0%'
                          '\nocc_att=12,400,000,000 USD'
                          '\nocc_lim=9,000,000,000 USD'
                          '\nnth=1'
                          '\nreinsts=[1.0/0.1]'
                          '\nfranchise=0 USD')
        terms, warning = visualizations._format_layer_terms(layer_view.layer)
        assert terms == expected_terms
        assert warning is False

    def test_order_of_all_terms(self, layer_view_with_all_terms):
        expected_terms = ('\ncoverage=[2017-01-01, 2018-02-02]'
                          '\nshare=30.0%'
                          '\nfilters=[\'One\']'
                          '\ninvert=False'
                          '\nocc_att=4 USD'
                          '\nocc_lim=5 USD'
                          '\nnth=6'
                          '\nreinsts=[0.8/0.07]'
                          '\nfranchise=10 USD'
                          '\nevent_lim=9 USD'
                          '\nagg_att=11 USD'
                          '\nagg_lim=12 USD'
                          '\nagg_period=13'
                          '\nagg_reset=14'
                          '\nsums_insured=15 USD'
                          '\nretained_line=16 USD'
                          '\nnumber_of_lines=17'
                          '\ntrigger=18 USD'
                          '\npayout_date=2018-12-19'
                          '\npayout=20 USD'
                          '\npremium=21 USD')
        terms, warning = visualizations._format_layer_terms(
            layer_view_with_all_terms)
        assert terms == expected_terms
        assert warning is False

    def test_attachment_warning(self, layer_view_attachment_warning):
        expected_terms = ('\nocc_att=unlimited')
        terms, warning = visualizations._format_layer_terms(
            layer_view_attachment_warning)
        assert warning is True
        assert terms == expected_terms

    def test_filter_warning(self, layer_view_filter_warning):
        terms, warning = visualizations._format_layer_terms(
            layer_view_filter_warning)
        expected_terms = ('\nfilters=(empty)'
                          '\ninvert=False')
        assert terms == expected_terms
        assert warning is True

    def test_participation_warning(self, layer_view_participation_warning):
        terms, warning = visualizations._format_layer_terms(
            layer_view_participation_warning)
        assert terms == '\nshare=0.0%'
        assert warning is True

    def test_unlimited_attachment(self):
        content = {'attachment': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nocc_att=unlimited'
        assert warning is True

    def test_unlimited_aggregate_attachment(self):
        content = {'aggregate_attachment': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nagg_att=unlimited'
        assert warning is True

    def test_unlimited_limit(self):
        content = {'limit': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\nocc_lim=unlimited'
        assert warning is False

    def test_null_premium(self):
        content = {'premium': None}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == ''
        assert warning is False

    def test_premium(self):
        content = {'premium': {
                     'value': 12500000.0,
                     'currency': 'USD',
                     'value_date': None,
                     'rate': None,
                     'rate_currency': None}
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, warning = visualizations._format_layer_terms(layer)
        assert terms == '\npremium=12,500,000 USD'
        assert warning is False


@pytest.fixture()
def default_LayerViewDigraph_args():
    default_args = {'_with_terms': True,
                    '_rankdir': 'BT',
                    '_format': 'png',
                    '_compact': True,
                    '_warnings': True,
                    '_max_depth': 0,
                    '_max_sources': 0,
                    '_colors': 1,
                    '_color_mode': 'breadth'}
    return default_args


@pytest.mark.usefixtures('default_LayerViewDigraph_args')
class TestLayerViewDigraph:

    def _get_filename(self, lv_id, **overrides):

        # merge the default arguments with the overrides
        args = default_LayerViewDigraph_args()
        args.update(overrides)
        compact = 'compact' if args['_compact'] else 'not-compact'
        terms = 'with-terms' if args['_with_terms'] else 'without-terms'
        warnings = ('warnings-enabled' if args['_warnings']
                    else 'warnings-disabled')
        depth = ('' if args['_max_depth'] == 0 else
                 '_depth-{}'.format(args['_max_depth']))
        src_limit = ('' if args['_max_sources'] == 0 else
                     '_srclimit-{}'.format(args['_max_sources']))
        colors = ('' if args['_colors'] == 1 else
                  '_{}-colors-by-{}'.format(args['_colors'],
                                            args['_color_mode']))
        filename = (args['_filename'] if '_filename' in args else
                    '{}_{}_{}_{}_{}{}{}{}'.format(lv_id,
                                                  args['_rankdir'],
                                                  compact,
                                                  terms,
                                                  warnings,
                                                  depth,
                                                  src_limit,
                                                  colors))
        return filename

    def _validate_args(self, lvg, **overrides):
        # merge the default arguments with the overrides
        args = default_LayerViewDigraph_args()
        args.update(overrides)

        # now that we have merged the defaults with the overrides, we will
        # compute the filename
        args['_filename'] = self._get_filename(lvg, **args)

        assert lvg._with_terms is args['_with_terms']
        assert lvg._rankdir == args['_rankdir']
        assert lvg._format == args['_format']
        assert lvg._compact is args['_compact']
        assert lvg._warnings is args['_warnings']
        assert lvg._colors is args['_colors']
        assert lvg._color_mode is args['_color_mode']

    def test_invalid_lv(self):
        m = {'something': 'here'}
        lv = convert_to_analyzere_object(m, Resource)
        with pytest.raises(ValueError):
            visualizations.LayerViewDigraph(lv)

    def test_basic(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # assert default arguments used for graph construction
        self._validate_args(lvg)

        expected_filename = self._get_filename(layer_view.id)
        assert lvg._filename == expected_filename

    def test_without_terms(self, layer_view):
        override = False
        lvg = visualizations.LayerViewDigraph(layer_view, with_terms=override)
        assert lvg._lv == layer_view
        # validate 'with_terms' override used for graph construction
        self._validate_args(lvg, _with_terms=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _with_terms=override)
        assert lvg._filename == expected_filename

    def test_with_compact(self, layer_view):
        override = True
        lvg = visualizations.LayerViewDigraph(layer_view, compact=override)
        assert lvg._lv == layer_view
        # verify 'compact' override used for graph construction
        self._validate_args(lvg, _compact=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _compact=override)
        assert lvg._filename == expected_filename

    def test_without_warnings(self, layer_view):
        override = False
        lvg = visualizations.LayerViewDigraph(layer_view, warnings=override)
        assert lvg._lv == layer_view
        # verify 'warnings' override used for graph construction
        self._validate_args(lvg, _warnings=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _warnings=override)
        assert lvg._filename == expected_filename

    def test_format(self, layer_view):
        override = 'pdf'
        lvg = visualizations.LayerViewDigraph(layer_view, format=override)
        assert lvg._lv == layer_view
        # verify 'format' override used for graph construction
        self._validate_args(lvg, _format=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _format=override)
        assert lvg._filename == expected_filename

    def test_max_depth(self, layer_view):
        override = 3
        lvg = visualizations.LayerViewDigraph(layer_view, max_depth=override)
        assert lvg._lv == layer_view
        # verify 'max_depth' override used for graph construction
        self._validate_args(lvg, _max_depth=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _max_depth=override)
        assert lvg._filename == expected_filename

    def test_max_sources(self, layer_view):
        override = 3
        lvg = visualizations.LayerViewDigraph(layer_view, max_sources=override)
        assert lvg._lv == layer_view
        # verify 'max_sources' override used for graph construction
        self._validate_args(lvg, _max_sources=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _max_sources=override)
        assert lvg._filename == expected_filename

    def test_with_colors(self, layer_view):
        override = 3
        lvg = visualizations.LayerViewDigraph(layer_view, colors=override)
        assert lvg._lv == layer_view
        # verify 'colors' override used for graph construction
        self._validate_args(lvg, _colors=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _colors=override)
        assert lvg._filename == expected_filename

    def test_with_colors_and_color_mode_depth(self, layer_view):
        colors_override = 3
        mode_override = 'depth'
        lvg = visualizations.LayerViewDigraph(layer_view,
                                              colors=colors_override,
                                              color_mode=mode_override)
        assert lvg._lv == layer_view
        # verify 'color' and 'color_mode' override used for graph construction
        self._validate_args(lvg,
                            _colors=colors_override,
                            _color_mode=mode_override)

        expected_filename = self._get_filename(layer_view.id,
                                               _colors=colors_override,
                                               _color_mode=mode_override)
        assert lvg._filename == expected_filename

    def test_render(self, layer_view):
        """Test that the expected (default) 'filename' parameter is passed to
        the underlying graphviz.render() method
        """
        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # verify default arguments used for graph construction
        self._validate_args(lvg)

        expected_filename = self._get_filename(layer_view.id)
        assert lvg._filename == expected_filename

        # mock out the underlying graphviz Digraph
        lvg._graph = Mock()

        lvg.render()
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename

    def test_render_without_terms(self, layer_view):
        """Test that the expected (default) 'filename' parameter is passed to
        the underlying graphviz.render() method
        """
        override = False
        lvg = visualizations.LayerViewDigraph(layer_view, with_terms=override)
        assert lvg._lv == layer_view
        # verify 'with_terms' override used for graph construction
        self._validate_args(lvg, _with_terms=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _with_terms=override)
        assert lvg._filename == expected_filename

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        lvg.render()
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename

    def test_render_compact(self, layer_view):
        """Test that the 'compact' parameter affects the filename
        that is is passed to the underlying graphviz.render() method
        """
        override = True
        lvg = visualizations.LayerViewDigraph(layer_view, compact=override)
        assert lvg._lv == layer_view
        # verify 'compact' override used for graph construction
        self._validate_args(lvg, _compact=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _compact=override)
        assert lvg._filename == expected_filename

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        lvg.render()
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename

    def test_render_with_view(self, layer_view):
        """Test that the 'compact' parameter affects the filename
        that is is passed to the underlying graphviz.render() method
        """
        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # verify default arguments used for graph construction
        self._validate_args(lvg)

        expected_filename = self._get_filename(layer_view.id)
        assert lvg._filename == expected_filename

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        lvg.render(view=True)
        lvg._graph.render.assert_called_with(expected_filename, view=True)
        assert lvg._filename == expected_filename

    def test_render_filename(self, layer_view):
        """Test that the 'filename' parameter is passed to the underlying
        graphviz.render() method
        """
        expected_filename = '{}_BT_with_terms'.format(layer_view.id)

        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # verify default arguments used for graph construction
        self._validate_args(lvg)

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        filename = 'my_graph'
        expected_filename = self._get_filename(layer_view.id,
                                               _filename=filename)

        lvg.render(filename=filename)
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename

    def test_render_format(self, layer_view):
        """Test that the 'format' parameter is passed to the underlying
        graphviz.render() method.
        """
        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # verify default arguments used for graph construction
        self._validate_args(lvg)

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        lvg.render(format='pdf')
        expected_filename = self._get_filename(layer_view.id)
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename
        assert lvg._format == 'pdf'

    def test_render_rankdir(self, layer_view):
        """Test that the 'rankdir' parameter is passed to the underlying
        graphviz.render() method and that it also affects the 'filename'
        that is passed.
        """
        lvg = visualizations.LayerViewDigraph(layer_view)
        assert lvg._lv == layer_view
        # verify default arguments used for graph construction
        self._validate_args(lvg)

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()
        lvg._graph.graph_attr = {}

        rankdir = 'TB'
        expected_filename = self._get_filename(layer_view.id,
                                               _rankdir=rankdir)
        lvg.render(rankdir=rankdir)
        lvg._graph.render.assert_called_with(expected_filename, view=False)
        assert lvg._filename == expected_filename
        assert lvg._graph.graph_attr['rankdir'] == 'TB'

    def test_from_id(self):
        """Requests by Id don't work unless you have defined the following
        analyzere varialbes, and a connecton can be established
           - analyzere.base_url
           - analyzere.username
           - analyzere.password
        """
        lvid = 'ee3f8420-c583-4dd4-9f9d-8ade29b0d82f'
        with pytest.raises(ConnectionError):
            visualizations.LayerViewDigraph.from_id(lvid)
