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
        },
        'target_currency': 'USD',
        'ylt_id': '9d61ecf9-9219-57ba-dd2a-fa515732639e'
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


class TestLayerTermsFormatter:
    def test_layer(self, layer_view):
        t, w = visualizations._format_layer_terms(layer_view)
        assert w is False

    def test_attachment_warning(self, layer_view_attachment_warning):
        t, w = visualizations._format_layer_terms(
            layer_view_attachment_warning)

    def test_filter_warning(self, layer_view_filter_warning):
        t, w = visualizations._format_layer_terms(layer_view_filter_warning)
        assert w is True

    def test_participation_warning(self, layer_view_participation_warning):
        t, w = visualizations._format_layer_terms(
            layer_view_participation_warning)
        assert w is True

    def test_coverage_inception_only(self):
        content = {'inception_date': datetime(2017, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[2017-01-01, inf]'

    def test_coverage_expriry_only(self):
        content = {'expiry_date': datetime(2018, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[-inf, 2018-01-01]'

    def test_full_coverage(self):
        content = {'inception_date': datetime(2017, 1, 1),
                   'expiry_date': datetime(2018, 1, 1)}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\ncoverage=[2017-01-01, 2018-01-01]'

    def test_unlimited_attachment(self):
        content = {'attachment': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nocc_att=unlimited'
        assert w is True

    def test_unlimited_aggregate_attachment(self):
        content = {'aggregate_attachment': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nagg_att=unlimited'
        assert w is True

    def test_unlimited_limit(self):
        content = {'limit': {
                     'currency': 'USD',
                     'value': float_info.max
                   }}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nocc_lim=unlimited'
        assert w is False

    def test_no_reinstatements(self):
        content = {'reinstatements': []}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == ''

    def test_four_reinstatements(self):
        content = {'reinstatements': [{'brokerage': 0.01, 'premium': 0.1},
                                      {'brokerage': 0.02, 'premium': 0.2},
                                      {'brokerage': 0.03, 'premium': 0.3},
                                      {'brokerage': 0.04, 'premium': 0.4}]
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nreinsts=[0.1/0.01, 0.2/0.02, 0.3/0.03, 0.4/0.04]'

    def test_many_reinstatements(self):
        content = {'reinstatements': [{'brokerage': 0.01, 'premium': 0.1},
                                      {'brokerage': 0.02, 'premium': 0.2},
                                      {'brokerage': 0.03, 'premium': 0.3},
                                      {'brokerage': 0.04, 'premium': 0.4},
                                      {'brokerage': 0.05, 'premium': 0.5}]
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nreinsts=5'

    def test_no_filters(self):
        content = {'filters': []}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=(empty)'

    def test_max_filters(self):
        content = {'filters': [{'name': 'One'},
                               {'name': 'Two'},
                               {'name': 'Three'}]}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=[\'One\', \'Two\', \'Three\']'

    def test_many_filters(self):
        content = {'filters': [{'name': 'One'},
                               {'name': 'Two'},
                               {'name': 'Three'},
                               {'name': 'Four'},
                               {'name': 'Five'}]}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\nfilters=(5 filters)'

    def test_null_premium(self):
        content = {'premium': None}
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == ''

    def test_premium(self):
        content = {'premium': {
                     'value': 12500000.0,
                     'currency': "USD",
                     'value_date': None,
                     'rate': None,
                     'rate_currency': None}
                   }
        layer = convert_to_analyzere_object(content, LayerView)
        terms, w = visualizations._format_layer_terms(layer)
        assert terms == '\npremium=12,500,000 USD'


@pytest.fixture()
def default_LayerViewDigraph_args():
    default_args = {'_with_terms': True,
                    '_rankdir': 'BT',
                    '_format': 'png',
                    '_verbose': False}
    return default_args


@pytest.mark.usefixtures('default_LayerViewDigraph_args')
class TestLayerViewDigraph:

    def _get_filename(self, lv_id, **overrides):

        # merge the default arguments with the overrides
        args = default_LayerViewDigraph_args()
        args.update(overrides)
        filename = (args['_filename'] if '_filename' in args else
                    '{}_{}{}{}'.format(lv_id,
                                       args['_rankdir'],
                                       '_verbose' if args['_verbose']
                                       else '',
                                       '_with_terms' if args['_with_terms']
                                       else ''))
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
        assert lvg._verbose is args['_verbose']

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

    def test_with_verbose(self, layer_view):
        override = True
        lvg = visualizations.LayerViewDigraph(layer_view, verbose=override)
        assert lvg._lv == layer_view
        # verify 'verbose' override used for graph construction
        self._validate_args(lvg, _verbose=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _verbose=override)
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
        lvg._graph.render.assert_called_with(expected_filename, view=True)
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
        lvg._graph.render.assert_called_with(expected_filename, view=True)
        assert lvg._filename == expected_filename

    def test_render_verbose(self, layer_view):
        """Test that the 'verbose' parameter affects the filename
        that is is passed to the underlying graphviz.render() method
        """
        override = True
        lvg = visualizations.LayerViewDigraph(layer_view, verbose=override)
        assert lvg._lv == layer_view
        # verify 'verbose' override used for graph construction
        self._validate_args(lvg, _verbose=override)

        expected_filename = self._get_filename(layer_view.id,
                                               _verbose=override)
        assert lvg._filename == expected_filename

        # mock out the underlying graphviz Digraph and ensure the appropriate
        # values are passed to its render() method
        lvg._graph = Mock()

        lvg.render()
        lvg._graph.render.assert_called_with(expected_filename, view=True)
        assert lvg._filename == expected_filename

    def test_render_without_view(self, layer_view):
        """Test that the 'verbose' parameter affects the filename
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

        lvg.render(view=False)
        lvg._graph.render.assert_called_with(expected_filename, view=False)
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
        lvg._graph.render.assert_called_with(expected_filename, view=True)
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
        lvg._graph.render.assert_called_with(expected_filename, view=True)
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
        lvg._graph.render.assert_called_with(expected_filename, view=True)
        assert lvg._filename == expected_filename
        assert lvg._graph.graph_attr['rankdir'] == 'TB'

    def test_fromId(self):
        """Requests by Id don't work unless you have defined the following
        analyzere varialbes, and a connecton can be established
           - analyzere.base_url
           - analyzere.username
           - analyzere.password
        """
        lvid = 'ee3f8420-c583-4dd4-9f9d-8ade29b0d82f'
        with pytest.raises(ConnectionError):
            visualizations.LayerViewDigraph.fromId(lvid)
