import pytest

from analyzere import LossSet
from analyzere_extras.combine_elts import ELTCombiner
from mock import patch


class AnalyzeReLossSetTestAPI():
    """Mocked Analyze Re API to control behaviour of API methods."""
    saved_counter = 0
    upload_data_input = None

    @classmethod
    def save(self):
        """Mocked 'LossSet.save()' function."""
        AnalyzeReLossSetTestAPI.saved_counter += 1
        self.id = 'ba5eball-{0}cal-dad{0}-ba5e-ba11coffee{0}'.format(
            AnalyzeReLossSetTestAPI.saved_counter)
        return self

    @classmethod
    def upload_data(self, file_like_obj):
        """Mocked 'LossSet.upload_data()' function."""
        self.status = 'processing_succeeded'
        self.status_message = None
        AnalyzeReLossSetTestAPI.upload_data_input = file_like_obj
        return self


class TestUploadCombinedELT:

    test_description = 'test description'
    fake_catalog = 'test catalog (should be an ARe object)'

    @patch.object(LossSet, 'upload_data', AnalyzeReLossSetTestAPI.upload_data)
    @patch.object(LossSet, 'save', AnalyzeReLossSetTestAPI.save)
    @pytest.mark.parametrize(
        'elt_response_key',
        ['elt_response_EventId', 'elt_response_EventID']
    )
    def test_event_id_column_names(
            self, elt_response_key, elt_response_dict):

        elt_combiner = ELTCombiner()

        elt_response = elt_response_dict[elt_response_key]

        assert len(elt_combiner._downloaded_elts) == 0
        elt_combiner._downloaded_elts = {}
        elt_combiner._downloaded_elts[elt_response[0]] = elt_response[1]
        elt_combiner._description = TestUploadCombinedELT.test_description
        elt_combiner._catalog = TestUploadCombinedELT.fake_catalog

        elt_combiner._upload_combined_elt()

        upload_data = AnalyzeReLossSetTestAPI.upload_data_input

        assert upload_data is not None
        assert len(upload_data) > 0

        upload_data = upload_data.replace(
            'EventId,Loss,STDDEVI,STDDEVC,EXPVALUE\n', '')

        expected_uploaded_data = []
        for row in elt_response[1][1:]:
            expected_uploaded_data.append('{},0.0,0.0,{}'.format(
                row,
                row.split(',')[1]
            ))

        assert upload_data == '\n'.join(expected_uploaded_data) + '\n'

    @patch.object(LossSet, 'upload_data', AnalyzeReLossSetTestAPI.upload_data)
    @patch.object(LossSet, 'save', AnalyzeReLossSetTestAPI.save)
    def test_uploaded_elt_has_proper_column_names(
            self, elt_response_1):

        elt_combiner = ELTCombiner()

        assert len(elt_combiner._downloaded_elts) == 0
        elt_combiner._downloaded_elts = {}
        elt_combiner._downloaded_elts[elt_response_1[0]] = elt_response_1[1]
        elt_combiner._description = TestUploadCombinedELT.test_description
        elt_combiner._catalog = TestUploadCombinedELT.fake_catalog

        elt_combiner._upload_combined_elt()

        upload_data = AnalyzeReLossSetTestAPI.upload_data_input

        assert upload_data is not None
        assert len(upload_data) > 0
        assert upload_data.startswith('EventId,Loss,STDDEVI,STDDEVC,EXPVALUE')

    @patch.object(LossSet, 'upload_data', AnalyzeReLossSetTestAPI.upload_data)
    @patch.object(LossSet, 'save', AnalyzeReLossSetTestAPI.save)
    def test_upload_combined_elt(
            self, elt_response_1, elt_response_2, elt_response_3):

        elt_combiner = ELTCombiner()
        elt_combiner._description = TestUploadCombinedELT.test_description
        elt_combiner._catalog = TestUploadCombinedELT.fake_catalog

        assert len(elt_combiner._downloaded_elts) == 0

        for elt_response in [elt_response_1, elt_response_2, elt_response_3]:
            elt_combiner._downloaded_elts[elt_response[0]] = \
                elt_response[1]

        assert len(elt_combiner._downloaded_elts) == 3

        elt_combiner._upload_combined_elt()

        upload_data = AnalyzeReLossSetTestAPI.upload_data_input

        assert upload_data is not None
        assert len(upload_data) > 0

        upload_data = upload_data.replace(
            'EventId,Loss,STDDEVI,STDDEVC,EXPVALUE\n', '')

        # Get appending order
        # (depends on dict elt_combiner._downloaded_elts items())
        elt_response_order = []
        for elt_id, elt_response in elt_combiner._downloaded_elts.items():
            elt_response_order.append(elt_response)

        expected_uploaded_data = []
        for elt_response in elt_response_order:
            for row in elt_response[1:]:
                expected_uploaded_data.append('{},0.0,0.0,{}'.format(
                    row,
                    row.split(',')[1]
                ))

        assert upload_data == '\n'.join(expected_uploaded_data) + '\n'

    @patch.object(LossSet, 'upload_data', AnalyzeReLossSetTestAPI.upload_data)
    @patch.object(LossSet, 'save', AnalyzeReLossSetTestAPI.save)
    def test_upload_combined_elt_with_optional_columns(
            self,
            elt_response_additional_columns_1,
            elt_response_additional_columns_2,
            elt_response_additional_columns_3):

        elt_combiner = ELTCombiner()
        elt_combiner._description = TestUploadCombinedELT.test_description
        elt_combiner._catalog = TestUploadCombinedELT.fake_catalog

        assert len(elt_combiner._downloaded_elts) == 0

        for elt_response in [elt_response_additional_columns_1,
                             elt_response_additional_columns_2,
                             elt_response_additional_columns_3]:
            elt_combiner._downloaded_elts[elt_response[0]] = elt_response[1]

        assert len(elt_combiner._downloaded_elts) == 3

        elt_combiner._upload_combined_elt()

        upload_data = AnalyzeReLossSetTestAPI.upload_data_input

        assert upload_data is not None
        assert len(upload_data) > 0

        upload_data = upload_data.replace(
            'EventId,Loss,STDDEVI,STDDEVC,EXPVALUE\n', '')

        # Get appending order
        # (depends on dict elt_combiner._downloaded_elts items())
        elt_response_order = []
        for elt_id, elt_response in elt_combiner._downloaded_elts.items():
            elt_response_order.append(elt_response)

        expected_uploaded_data = []
        for elt_response in elt_response_order:
            for row in elt_response[1:]:
                expected_uploaded_data.append(row)

        assert upload_data == '\n'.join(expected_uploaded_data) + '\n'
