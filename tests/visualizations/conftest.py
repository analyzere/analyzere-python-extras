import pytest
import uuid

from analyzere.base_resources import convert_to_analyzere_object
from analyzere import LayerView
from datetime import datetime
from sys import float_info


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


@pytest.fixture()
def default_LayerViewDigraph_args():
    default_args = {
        '_with_terms': True,
        '_rankdir': 'BT',
        '_format': 'png',
        '_compact': True,
        '_warnings': True,
        '_max_depth': 0,
        '_max_sources': 0,
        '_colors': 1,
        '_color_mode': 'breadth'}
    return default_args
