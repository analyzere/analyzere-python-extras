import pytest

from analyzere.base_resources import convert_to_analyzere_object
from analyzere import utils
from analyzere_extras import visualizations
from datetime import datetime
from sys import float_info


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

    def test_basic(self):
        pass

    def test_with_terms(self):
        pass

    def test_format(self):
        pass

    def test_render_filename(self):
        pass

    def test_render_format(self):
        pass

    def test_render_rankdir(self):
        pass

    def test_fromId(self):
        pass

