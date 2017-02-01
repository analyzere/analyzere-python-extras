import pytest
import os
import uuid

from analyzere.base_resources import convert_to_analyzere_object, Resource
from analyzere import utils, LayerView
from analyzere_extras import visualizations
from datetime import datetime
from requests import ConnectionError
from sys import float_info

@pytest.fixture(scope='session')
def layer_view():
    content = {
        "analysis_profile": {
            "ref_id": "4e5bccc9-3ad3-4231-8205-1120c4180daf"
        },
        "id": str(uuid.uuid4()),
        "layer": {
          "_type": "CatXL",
          "description" : "9x12.4 CatXL",
          "attachment": {
            "currency": "USD",
            "value": 12400000000.0,
            },
          "franchise": {
           "currency": "USD",
            "value": 0.0,
            },
          "limit": {
            "currency": "USD",
            "value": 9000000000.0,
            },
          "loss_sets": [
            {
              "_type": "YELTLossSet",
              "created": "2017-01-17T01:01:01.966052+00:00",
              "currency": "USD",
              "data": {
                "ref_id": "389e169e-d671-49e5-91ae-3c4a8ed1fcad"
              },
              "data_type": "csv",
              "description": "Illinois US ST RES",
              "event_catalogs": [
                {
                  "ref_id": "c508b867-6d6b-4eaf-aad5-294c4debf6de"
                }
              ],
              "id": "e60a747e-0556-41ce-9ab9-2102f629f559",
              "loss_type": "LossGross",
              "modified": "2017-01-17T01:01:16.237408+00:00",
              "profile": {
                "attributes": {
                  "Country": ["US" ],
                  "Peril": [ "ST" ],
                  "Region": ["North America"],
                  "SubRegion": ["AB","WY"]
                  },
                "avg_annual_loss": 555259274.678332,
                "currency": "USD",
                "max_loss": 19909099444.0,
                "min_loss": 0.0,
                "non_zero_losses": 133674,
                "num_losses": 133700
                },
              "start_date": "2017-01-01T00:00:00+00:00",
              "status": "processing_succeeded",
              "trial_count": 10000
            },
            {
              "_type": "YELTLossSet",
              "created": "2017-01-17T00:20:08.805598+00:00",
              "currency": "USD",
              "data": {
                "ref_id": "c28046b7-5a5d-43a9-9324-7327bbd934de"
              },
              "data_type": "csv",
              "description": "Nova Scotia Canada EQ COM",
              "event_catalogs": [
                {
                   "ref_id": "c508b867-6d6b-4eaf-aad5-294c4debf6de"
                }
              ],
              "id": "8bfc42b8-75ed-450a-b474-4f936b449dc3",
              "loss_type": "LossGross",
              "modified": "2017-01-17T00:20:18.231491+00:00",
              "profile": {
                "attributes": {
                  "Country": ["Canada"],
                  "Peril": ["EQ"],
                  "Region": ["North America"],
                  "SubRegion": ["NB", "NS","PE"]
                },
                "avg_annual_loss": 5591.573225,
                "currency": "USD",
                "max_loss": 51649446.69,
                "min_loss": 4.66,
                "non_zero_losses": 24,
                "num_losses": 24
              },
              "start_date": "2017-01-01T00:00:00+00:00",
              "status": "processing_succeeded",
              "trial_count": 10000
            }
          ],
          "meta_data": {},
          "nth": 1,
          "participation": 1.0,
          "reinstatements": [
            {
              "brokerage": 0.1,
              "premium": 1.0
              }
          ]
        },
        "target_currency": "USD",
        "ylt_id": "9d61ecf9-9219-57ba-dd2a-fa515732639e"
    }
    return convert_to_analyzere_object(content, LayerView)

class TestDescriptionFormatter:
    def test_description_with_colon(self):
        raw = 'auto: FilterLayer USHU'
        expected = 'auto: FilterLayer USHU'
        assert visualizations._format_description(raw) == expected

    def test_description_with_windows_file_path(self):
        raw = 'Layer 2 : Z:\\losses\\alpha.csv'
        expected = 'Layer 2 : Z:\\\\losses\\\\alpha.csv'
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


class TestLayerViewDigraph:
    def test_invalid_lv(self):
        m = {'something': 'here'}
        lv = convert_to_analyzere_object(m, Resource)
        with pytest.raises(ValueError):
            lvg = visualizations.LayerViewDigraph(lv)

    def test_basic(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)

    def test_without_terms(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view, with_terms=False)
        assert lvg._with_terms == False

    def test_without_verbose(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view, verbose=True)
        assert lvg._verbose == True

    def test_format(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view, format='pdf')
        assert lvg._graph.format == 'pdf'
        lvg = visualizations.LayerViewDigraph(layer_view, format='svg')
        assert lvg._graph.format == 'svg'

    def test_render(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)
        fn = lvg.render(view=False)
        expected_filename = '{}-with_terms-BT.png'.format(layer_view.id)
        assert fn == expected_filename
        os.remove(expected_filename)

        fn = ''
        expected_filename = '{}-with_terms-BT.png'.format(layer_view.id)
        fn = visualizations.LayerViewDigraph(layer_view).render(view=False)
        assert fn == expected_filename
        os.remove(expected_filename)
        os.remove(os.path.splitext(expected_filename)[0])

    def test_render_without_terms(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view, with_terms=False)
        fn = lvg.render(view=False)
        expected_filename = '{}-BT.png'.format(layer_view.id)
        assert fn == expected_filename
        os.remove(expected_filename)
        os.remove(os.path.splitext(expected_filename)[0])

    def test_render_filename(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)
        filename = 'my_graph'
        fn = lvg.render(filename=filename, view=False)
        expected_filename = '{}.png'.format(filename)
        assert fn == expected_filename
        os.remove(expected_filename)
        os.remove(os.path.splitext(expected_filename)[0])

    def test_render_format(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)
        fn = lvg.render(format='pdf', view=False)
        expected_filename = '{}-with_terms-BT.pdf'.format(layer_view.id)
        assert fn == expected_filename
        os.remove(expected_filename)
        os.remove(os.path.splitext(expected_filename)[0])

    def test_render_rankdir(self, layer_view):
        lvg = visualizations.LayerViewDigraph(layer_view)
        rankdir = 'TB'
        fn = lvg.render(rankdir=rankdir, view=False)
        expected_filename = '{}-with_terms-{}.png'.format(layer_view.id,
                                                          rankdir)
        assert fn == expected_filename
        os.remove(expected_filename)
        os.remove(os.path.splitext(expected_filename)[0])

    def test_fromId(self):
        """Requests by Id don't work unless you have defined the following
        analyzere varialbes, and a connecton can be established
           - analyzere.base_url
           - analyzere.username
           - analyzere.password
        """
        lvid = 'ee3f8420-c583-4dd4-9f9d-8ade29b0d82f'
        with pytest.raises(ConnectionError):
            lvg = visualizations.LayerViewDigraph.fromId(lvid)
