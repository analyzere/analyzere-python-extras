import requests_mock
from analyzere_extras.loss_sets import AnalogousEventLossSet
import analyzere
from analyzere import AnalysisProfile


def are_mocker():
    m = requests_mock.Mocker()
    m.start()
    m.register_uri(
        'POST',
        'https://api/layer_views/',
        [{'status_code': 200, 'text': '{"id": "1"}'},
         {'status_code': 200, 'text': '{"id": "2"}'},
         {'status_code': 200, 'text': '{"id": "3"}'},
         {'status_code': 200, 'text': '{"id": "4"}'}]
    )

    m.get('https://api/layer_views/1/yelt?secondary_uncertainty=false',
          status_code=200,
          text="""Trial,EventId,Sequence,Loss
          1,1,0.0,100.0""")

    m.get('https://api/layer_views/2/yelt?secondary_uncertainty=false',
          status_code=200,
          text='Trial,EventId,Sequence,Loss')

    m.get('https://api/layer_views/3/yelt?secondary_uncertainty=false',
          status_code=200,
          text="""Trial,EventId,Sequence,Loss
          1,3,0.0,100.0
          2,3,0.0,50.0""")

    m.get('https://api/layer_views/4/yelt?secondary_uncertainty=false',
          status_code=200,
          text="""Trial,EventId,Sequence,Loss
          1,4,0.0,200.0""")

    # Mocking Distribution Uploads
    # Distributions.save()
    m.register_uri(
        'POST',
        'https://api/distributions/',
        [{'status_code': 200, 'text': '{"id": "d1"}'},
         {'status_code': 200, 'text': '{"id": "d2"}'},
         {'status_code': 200, 'text': '{"id": "d3"}'}]
    )

    # Distributions.list(...)
    m.get('https://api/distributions/?', status_code=200, text='[]')

    # Distribution.upload_data()
    m.post('https://api/distributions/d1/data', status_code=201, text='data')
    m.patch('https://api/distributions/d1/data', status_code=204)
    m.post('https://api/distributions/d1/data/commit', status_code=204)
    m.get('https://api/distributions/d1/data/status', status_code=200,
          text='{"status": "Processing Successful"}')

    # LossSet.save()
    m.post('https://api/loss_sets/', status_code=200,
           text='{"id": "ls1", "server_generate": "foo"}')

    return m


class SetBaseUrl(object):
    def setup_method(self, _):
        analyzere.base_url = 'https://api'

    def teardown_method(self, _):
        analyzere.base_url = 'http://localhost:8000/'


class TestAnalogousEventLossSet(SetBaseUrl):
    def test_null_construction(self):
        ae_ls = AnalogousEventLossSet()
        assert ae_ls.type == 'ParametricLossSet'
        assert ae_ls.analysis_profile == ''
        assert ae_ls.load == 1.0
        assert ae_ls.sources == []
        assert ae_ls.source_events == []
        assert ae_ls.occurrence_probability == 1.0

    def test_retrieve_loss_data(self):
        m = are_mocker()
        ae_ls = AnalogousEventLossSet(sources=['abc123'], source_events=[1])
        ae_ls._retrieve_loss_data()
        m.stop()
        assert ae_ls._loss_data == {1: [100.0]}

        m = are_mocker()
        ae_ls = AnalogousEventLossSet(sources=['abc123'], source_events=[1, 2])
        ae_ls._retrieve_loss_data()
        m.stop()
        assert ae_ls._loss_data == {1: [100.0], 2: []}

    def test_severity_distribution(self):
        m = are_mocker()
        ae_ls = AnalogousEventLossSet(source_events=[1])
        ae_ls._retrieve_loss_data()
        ae_ls._construct_severity_distribution()
        m.stop()
        assert ae_ls._severity_distr == "Probability,Loss\n1.0,100.0\n"

        m = are_mocker()
        ae_ls = AnalogousEventLossSet(source_events=[1, 2])
        ae_ls._retrieve_loss_data()
        ae_ls._construct_severity_distribution()
        m.stop()
        assert ae_ls._severity_distr == \
            "Probability,Loss\n0.5,0.0\n0.5,100.0\n"

        m = are_mocker()
        ae_ls = AnalogousEventLossSet(source_events=[1, 2, 3, 4])
        ae_ls._retrieve_loss_data()
        ae_ls._construct_severity_distribution()
        m.stop()
        assert (ae_ls._severity_distr == 'Probability,Loss\n'
                + '0.25,0.0\n0.125,50.0\n0.375,100.0\n0.25,200.0\n')

    def test_save(self):
        m = are_mocker()
        ae_ls = AnalogousEventLossSet(
            analysis_profile=AnalysisProfile(id='ap1'),
            source_events=[1]
        )
        ae_ls.save()
        m.stop()
        for attribute in ['analysis_profile', 'source_events', 'sources',
                          'load', 'occurrence_probability']:
            assert hasattr(ae_ls, attribute)
