import pytest

from analyzere.base_resources import convert_to_analyzere_object


@pytest.fixture(scope='session')
def portfolio():

    portfolio_dict = {
        '_type': 'StaticPortfolio',
        'created': '2016-03-09T18:38:04.801820Z',
        'description': 'Charlie Group 2019',
        'id': '05f80984-5cc5-4954-a88c-e2317d1dbe37',
        'layers': [
            {
                '_type': 'CatXL',
                'attachment': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 500000.0,
                    'value_date': None
                },
                'created': '2016-03-09T18:38:04.801820Z',
                'description': 'Model A - Charlie Group Layer 1',
                'expiry_date': '2017-01-01T00:00:00.000000Z',
                'fees': None,
                'franchise': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 0.0,
                    'value_date': None
                },
                'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
                'inception_date': '2016-01-01T00:00:00.000000Z',
                'limit': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 500000.0,
                    'value_date': None
                },
                'loss_sets': [
                    {
                        '_type': 'ELTLossSet',
                        'created': '2016-03-09T18:38:04.801820Z',
                        'currency': 'USD',
                        'data': {
                            'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                        },
                        'description': 'FL_HU_Program_1',
                        'event_catalogs': [
                            {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                        ],
                        'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
                        'loss_type': 'LossGross',
                        'meta_data': {},
                        'modified': '2016-03-09T18:38:04.801820Z',
                        'profile': {
                            'attributes': {
                                'ModelID': ['1'],
                                'Peril': ['HU'],
                                'Region': ['US'],
                                'SubRegion': ['Florida']
                            },
                            'avg_annual_loss': 446831.486739948,
                            'currency': 'USD',
                            'max_loss': 8995286.82877091,
                            'min_loss': 10553.9672063884,
                            'non_zero_losses': 1000,
                            'num_losses': 1000
                        },
                        'status': 'processing_succeeded',
                        'status_message': None
                    },
                    {
                        '_type': 'ELTLossSet',
                        'created': '2016-03-09T18:38:04.801820Z',
                        'currency': 'USD',
                        'data': {
                            'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                        },
                        'description': 'FL_HU_Program_1',
                        'event_catalogs': [
                            {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                        ],
                        'id': 'a3bbebae-d25d-493e-8c02-fa4305e7dbd0',
                        'loss_type': 'LossGross',
                        'meta_data': {},
                        'modified': '2016-03-09T18:38:04.801820Z',
                        'profile': {
                            'attributes': {
                                'ModelID': ['1'],
                                'Peril': ['HU'],
                                'Region': ['US'],
                                'SubRegion': ['Florida']
                            },
                            'avg_annual_loss': 446831.486739948,
                            'currency': 'USD',
                            'max_loss': 8995286.82877091,
                            'min_loss': 10553.9672063884,
                            'non_zero_losses': 1000,
                            'num_losses': 1000
                        },
                        'status': 'processing_succeeded',
                        'status_message': None
                    }
                ],
                'meta_data': {
                    'business_unit': 'North America',
                    'cat_modeler': 'Elizabeth Hawks',
                    'client_id': 'Model A - Charlie Group Layer 1',
                    'peril': 'EQ',
                    'program_id': 3,
                    'program_name': 'Charlie Group',
                    'region': 'California',
                    'underwriter': 'Travis Costa'
                },
                'modified': '2016-03-09T18:38:04.801820Z',
                'nth': 1,
                'participation': 0.092,
                'policy': None,
                'premium': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 39939.9225,
                    'value_date': None
                },
                'reinstatements': []
            },
            {
                '_type': 'CatXL',
                'attachment': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 500000.0,
                    'value_date': None
                },
                'created': '2016-03-09T18:38:04.801820Z',
                'description': 'Model A - Charlie Group Layer 1',
                'expiry_date': '2017-01-01T00:00:00.000000Z',
                'fees': None,
                'franchise': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 0.0,
                    'value_date': None
                },
                'id': '286226d2-e0c8-4ecf-b6cf-ba381789fbd2',
                'inception_date': '2016-01-01T00:00:00.000000Z',
                'limit': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 500000.0,
                    'value_date': None
                },
                'loss_sets': [
                    {
                        '_type': 'ELTLossSet',
                        'created': '2016-03-09T18:38:04.801820Z',
                        'currency': 'USD',
                        'data': {
                            'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                        },
                        'description': 'FL_HU_Program_1',
                        'event_catalogs': [
                            {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                        ],
                        'id': '5c468e85-3716-4abb-87b2-bcd39f6d6afd',
                        'loss_type': 'LossGross',
                        'meta_data': {},
                        'modified': '2016-03-09T18:38:04.801820Z',
                        'profile': {
                            'attributes': {
                                'ModelID': ['1'],
                                'Peril': ['HU'],
                                'Region': ['US'],
                                'SubRegion': ['Florida']
                            },
                            'avg_annual_loss': 446831.486739948,
                            'currency': 'USD',
                            'max_loss': 8995286.82877091,
                            'min_loss': 10553.9672063884,
                            'non_zero_losses': 1000,
                            'num_losses': 1000
                        },
                        'status': 'processing_succeeded',
                        'status_message': None
                    },
                    {
                        '_type': 'ELTLossSet',
                        'created': '2016-03-09T18:38:04.801820Z',
                        'currency': 'USD',
                        'data': {
                            'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                        },
                        'description': 'FL_HU_Program_1',
                        'event_catalogs': [
                            {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                        ],
                        'id': 'c1c0d452-1dd1-44a6-8489-4de06c0a1b58',
                        'loss_type': 'LossGross',
                        'meta_data': {},
                        'modified': '2016-03-09T18:38:04.801820Z',
                        'profile': {
                            'attributes': {
                                'ModelID': ['1'],
                                'Peril': ['HU'],
                                'Region': ['US'],
                                'SubRegion': ['Florida']
                            },
                            'avg_annual_loss': 446831.486739948,
                            'currency': 'USD',
                            'max_loss': 8995286.82877091,
                            'min_loss': 10553.9672063884,
                            'non_zero_losses': 1000,
                            'num_losses': 1000
                        },
                        'status': 'processing_succeeded',
                        'status_message': None
                    }
                ],
                'meta_data': {
                    'business_unit': 'North America',
                    'cat_modeler': 'Elizabeth Hawks',
                    'client_id': 'Model A - Charlie Group Layer 1',
                    'peril': 'EQ',
                    'program_id': 3,
                    'program_name': 'Charlie Group',
                    'region': 'California',
                    'underwriter': 'Travis Costa'
                },
                'modified': '2016-03-09T18:38:04.801820Z',
                'nth': 1,
                'participation': 0.092,
                'policy': None,
                'premium': {
                    'currency': 'USD',
                    'rate': None,
                    'rate_currency': None,
                    'value': 39939.9225,
                    'value_date': None
                },
                'reinstatements': []
            }
        ],
        'meta_data': {},
        'modified': '2016-03-09T18:38:04.801820Z',
        'name': 'Charlie Group 2019'
    }

    analyzere_portfolio = convert_to_analyzere_object(portfolio_dict)

    return [
        '05f80984-5cc5-4954-a88c-e2317d1dbe37',
        [
            '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
            'a3bbebae-d25d-493e-8c02-fa4305e7dbd0',
            '5c468e85-3716-4abb-87b2-bcd39f6d6afd',
            'c1c0d452-1dd1-44a6-8489-4de06c0a1b58'
        ],
        analyzere_portfolio
    ]


@pytest.fixture(scope='session')
def portfolio_view_with_layer_views():

    portfolio_view_dict = {
        'analysis_profile': {'ref_id': '3bb4950c-777f-44dd-a5c2-73a2dfa04d26'},
        'id': '3c9c86e3-56ab-447b-9008-d6d95adb0d11',
        'portfolio': None,
        'layer_views': [
            {
                'analysis_profile': {
                    'ref_id': '3bb4950c-777f-44dd-a5c2-73a2dfa04d26'
                },
                'id': '333bf15d-225a-a30c-b95d-22fff4722b5d',
                'layer': {
                    '_type': 'CatXL',
                    'attachment': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'created': '2016-03-09T18:38:04.801820Z',
                    'description': 'Model A - Charlie Group Layer 1',
                    'expiry_date': '2017-01-01T00:00:00.000000Z',
                    'fees': None,
                    'franchise': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 0.0,
                        'value_date': None
                    },
                    'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
                    'inception_date': '2016-01-01T00:00:00.000000Z',
                    'limit': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'loss_sets': [
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        }
                    ],
                    'meta_data': {
                        'business_unit': 'North America',
                        'cat_modeler': 'Elizabeth Hawks',
                        'client_id': 'Model A - Charlie Group Layer 1',
                        'peril': 'EQ',
                        'program_id': 3,
                        'program_name': 'Charlie Group',
                        'region': 'California',
                        'underwriter': 'Travis Costa'
                    },
                    'modified': '2016-03-09T18:38:04.801820Z',
                    'nth': 1,
                    'participation': 0.092,
                    'policy': None,
                    'premium': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 39939.9225,
                        'value_date': None
                    },
                    'reinstatements': []
                },
                'target_currency': 'USD',
                'ylt_id': '99838575-6a3c-a7a2-d1e5-40a8e1b67b47'
            },
            {
                'analysis_profile': {
                    'ref_id': '3bb4950c-777f-44dd-a5c2-73a2dfa04d26'
                },
                'id': 'fd4fe20c-fd04-4b85-bc65-67568be37d43',
                'layer': {
                    '_type': 'CatXL',
                    'attachment': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'created': '2016-03-09T18:38:04.801820Z',
                    'description': 'Model A - Charlie Group Layer 1',
                    'expiry_date': '2017-01-01T00:00:00.000000Z',
                    'fees': None,
                    'franchise': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 0.0,
                        'value_date': None
                    },
                    'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
                    'inception_date': '2016-01-01T00:00:00.000000Z',
                    'limit': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'loss_sets': [
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': 'acbdb659-b4b2-4784-873c-79952c071e97',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        }
                    ],
                    'meta_data': {
                        'business_unit': 'North America',
                        'cat_modeler': 'Elizabeth Hawks',
                        'client_id': 'Model A - Charlie Group Layer 1',
                        'peril': 'EQ',
                        'program_id': 3,
                        'program_name': 'Charlie Group',
                        'region': 'California',
                        'underwriter': 'Travis Costa'
                    },
                    'modified': '2016-03-09T18:38:04.801820Z',
                    'nth': 1,
                    'participation': 0.092,
                    'policy': None,
                    'premium': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 39939.9225,
                        'value_date': None
                    },
                    'reinstatements': []
                },
                'target_currency': 'USD',
                'ylt_id': '99838575-6a3c-a7a2-d1e5-40a8e1b67b47'
            }
        ],
        'target_currency': 'USD',
        'ylt_id': '99838575-6a3c-a7a2-d1e5-40a8e1b67b47'
    }

    analyzere_portfolio_view = convert_to_analyzere_object(portfolio_view_dict)

    return [
        '3c9c86e3-56ab-447b-9008-d6d95adb0d11',
        [
            '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
            'acbdb659-b4b2-4784-873c-79952c071e97'
        ],
        analyzere_portfolio_view
    ]


@pytest.fixture(scope='session')
def portfolio_view_with_portfolio():

    portfolio_view_dict = {
        'analysis_profile': {'ref_id': '3bb4950c-777f-44dd-a5c2-73a2dfa04d26'},
        'id': '7397662d-2be0-47c4-8956-b7f6e3c56c6c',
        'portfolio': {
            '_type': 'StaticPortfolio',
            'created': '2016-03-09T18:38:04.801820Z',
            'description': 'Charlie Group 2019',
            'id': '05f80984-5cc5-4954-a88c-e2317d1dbe37',
            'layers': [
                {
                    '_type': 'CatXL',
                    'attachment': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'created': '2016-03-09T18:38:04.801820Z',
                    'description': 'Model A - Charlie Group Layer 1',
                    'expiry_date': '2017-01-01T00:00:00.000000Z',
                    'fees': None,
                    'franchise': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 0.0,
                        'value_date': None
                    },
                    'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
                    'inception_date': '2016-01-01T00:00:00.000000Z',
                    'limit': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'loss_sets': [
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        },
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': 'a3bbebae-d25d-493e-8c02-fa4305e7dbd0',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        }
                    ],
                    'meta_data': {
                        'business_unit': 'North America',
                        'cat_modeler': 'Elizabeth Hawks',
                        'client_id': 'Model A - Charlie Group Layer 1',
                        'peril': 'EQ',
                        'program_id': 3,
                        'program_name': 'Charlie Group',
                        'region': 'California',
                        'underwriter': 'Travis Costa'
                    },
                    'modified': '2016-03-09T18:38:04.801820Z',
                    'nth': 1,
                    'participation': 0.092,
                    'policy': None,
                    'premium': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 39939.9225,
                        'value_date': None
                    },
                    'reinstatements': []
                },
                {
                    '_type': 'CatXL',
                    'attachment': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'created': '2016-03-09T18:38:04.801820Z',
                    'description': 'Model A - Charlie Group Layer 1',
                    'expiry_date': '2017-01-01T00:00:00.000000Z',
                    'fees': None,
                    'franchise': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 0.0,
                        'value_date': None
                    },
                    'id': '286226d2-e0c8-4ecf-b6cf-ba381789fbd2',
                    'inception_date': '2016-01-01T00:00:00.000000Z',
                    'limit': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 500000.0,
                        'value_date': None
                    },
                    'loss_sets': [
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': '5c468e85-3716-4abb-87b2-bcd39f6d6afd',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        },
                        {
                            '_type': 'ELTLossSet',
                            'created': '2016-03-09T18:38:04.801820Z',
                            'currency': 'USD',
                            'data': {
                                'ref_id':
                                    'd99999e4-d66e-4c0a-a6ba-554a8598fea5'
                            },
                            'description': 'FL_HU_Program_1',
                            'event_catalogs': [
                                {'ref_id':
                                    'aa8c316c-128c-485b-9144-5eed3f051c36'}
                            ],
                            'id': 'c1c0d452-1dd1-44a6-8489-4de06c0a1b58',
                            'loss_type': 'LossGross',
                            'meta_data': {},
                            'modified': '2016-03-09T18:38:04.801820Z',
                            'profile': {
                                'attributes': {
                                    'ModelID': ['1'],
                                    'Peril': ['HU'],
                                    'Region': ['US'],
                                    'SubRegion': ['Florida']
                                },
                                'avg_annual_loss': 446831.486739948,
                                'currency': 'USD',
                                'max_loss': 8995286.82877091,
                                'min_loss': 10553.9672063884,
                                'non_zero_losses': 1000,
                                'num_losses': 1000
                            },
                            'status': 'processing_succeeded',
                            'status_message': None
                        }
                    ],
                    'meta_data': {
                        'business_unit': 'North America',
                        'cat_modeler': 'Elizabeth Hawks',
                        'client_id': 'Model A - Charlie Group Layer 1',
                        'peril': 'EQ',
                        'program_id': 3,
                        'program_name': 'Charlie Group',
                        'region': 'California',
                        'underwriter': 'Travis Costa'
                    },
                    'modified': '2016-03-09T18:38:04.801820Z',
                    'nth': 1,
                    'participation': 0.092,
                    'policy': None,
                    'premium': {
                        'currency': 'USD',
                        'rate': None,
                        'rate_currency': None,
                        'value': 39939.9225,
                        'value_date': None
                    },
                    'reinstatements': []
                }
            ],
            'meta_data': {},
            'modified': '2016-03-09T18:38:04.801820Z',
            'name': 'Charlie Group 2019'
        },
        'target_currency': 'USD',
        'ylt_id': '99838575-6a3c-a7a2-d1e5-40a8e1b67b47'
    }

    analyzere_portfolio_view = convert_to_analyzere_object(portfolio_view_dict)

    return [
        '7397662d-2be0-47c4-8956-b7f6e3c56c6c',
        [
            '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
            'a3bbebae-d25d-493e-8c02-fa4305e7dbd0',
            '5c468e85-3716-4abb-87b2-bcd39f6d6afd',
            'c1c0d452-1dd1-44a6-8489-4de06c0a1b58'
        ],
        analyzere_portfolio_view
    ]


@pytest.fixture(scope='session')
def layer():
    layer_dict = {
        '_type': 'CatXL',
        'attachment': {
            'currency': 'USD',
            'rate': None,
            'rate_currency': None,
            'value': 500000.0,
            'value_date': None
        },
        'created': '2016-03-09T18:38:04.801820Z',
        'description': 'Model A - Charlie Group Layer 1',
        'expiry_date': '2017-01-01T00:00:00.000000Z',
        'fees': None,
        'franchise': {
            'currency': 'USD',
            'rate': None,
            'rate_currency': None,
            'value': 0.0,
            'value_date': None
        },
        'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
        'inception_date': '2016-01-01T00:00:00.000000Z',
        'limit': {
            'currency': 'USD',
            'rate': None,
            'rate_currency': None,
            'value': 500000.0,
            'value_date': None
        },
        'loss_sets': [
            {
                '_type': 'ELTLossSet',
                'created': '2016-03-09T18:38:04.801820Z',
                'currency': 'USD',
                'data': {'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'},
                'description': 'FL_HU_Program_1',
                'event_catalogs': [
                    {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                ],
                'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
                'loss_type': 'LossGross',
                'meta_data': {},
                'modified': '2016-03-09T18:38:04.801820Z',
                'profile': {
                    'attributes': {
                        'ModelID': ['1'],
                        'Peril': ['HU'],
                        'Region': ['US'],
                        'SubRegion': ['Florida']
                    },
                    'avg_annual_loss': 446831.486739948,
                    'currency': 'USD',
                    'max_loss': 8995286.82877091,
                    'min_loss': 10553.9672063884,
                    'non_zero_losses': 1000,
                    'num_losses': 1000
                },
                'status': 'processing_succeeded',
                'status_message': None
            },
            {
                '_type': 'ELTLossSet',
                'created': '2016-03-09T18:38:04.801820Z',
                'currency': 'USD',
                'data': {'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'},
                'description': 'FL_HU_Program_1',
                'event_catalogs': [
                    {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                ],
                'id': 'a3bbebae-d25d-493e-8c02-fa4305e7dbd0',
                'loss_type': 'LossGross',
                'meta_data': {},
                'modified': '2016-03-09T18:38:04.801820Z',
                'profile': {
                    'attributes': {
                        'ModelID': ['1'],
                        'Peril': ['HU'],
                        'Region': ['US'],
                        'SubRegion': ['Florida']
                    },
                    'avg_annual_loss': 446831.486739948,
                    'currency': 'USD',
                    'max_loss': 8995286.82877091,
                    'min_loss': 10553.9672063884,
                    'non_zero_losses': 1000,
                    'num_losses': 1000
                },
                'status': 'processing_succeeded',
                'status_message': None
            }
        ],
        'meta_data': {
            'business_unit': 'North America',
            'cat_modeler': 'Elizabeth Hawks',
            'client_id': 'Model A - Charlie Group Layer 1',
            'peril': 'EQ',
            'program_id': 3,
            'program_name': 'Charlie Group',
            'region': 'California',
            'underwriter': 'Travis Costa'
        },
        'modified': '2016-03-09T18:38:04.801820Z',
        'nth': 1,
        'participation': 0.092,
        'policy': None,
        'premium': {
            'currency': 'USD',
            'rate': None,
            'rate_currency': None,
            'value': 39939.9225,
            'value_date': None
        },
        'reinstatements': []
    }

    analyzere_layer = convert_to_analyzere_object(layer_dict)

    return [
        '07a98f2a-87c0-49d8-a98d-deb626707da2',
        [
            '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
            'a3bbebae-d25d-493e-8c02-fa4305e7dbd0'
        ],
        analyzere_layer
    ]


@pytest.fixture(scope='session')
def layer_view():
    layer_view_dict = {
        'analysis_profile': {'ref_id': '3bb4950c-777f-44dd-a5c2-73a2dfa04d26'},
        'id': '333bf15d-225a-a30c-b95d-22fff4722b5d',
        'layer': {
            '_type': 'CatXL',
            'attachment': {
                'currency': 'USD',
                'rate': None,
                'rate_currency': None,
                'value': 500000.0,
                'value_date': None
            },
            'created': '2016-03-09T18:38:04.801820Z',
            'description': 'Model A - Charlie Group Layer 1',
            'expiry_date': '2017-01-01T00:00:00.000000Z',
            'fees': None,
            'franchise': {
                'currency': 'USD',
                'rate': None,
                'rate_currency': None,
                'value': 0.0,
                'value_date': None
            },
            'id': '07a98f2a-87c0-49d8-a98d-deb626707da2',
            'inception_date': '2016-01-01T00:00:00.000000Z',
            'limit': {
                'currency': 'USD',
                'rate': None,
                'rate_currency': None,
                'value': 500000.0,
                'value_date': None
            },
            'loss_sets': [
                {
                    '_type': 'ELTLossSet',
                    'created': '2016-03-09T18:38:04.801820Z',
                    'currency': 'USD',
                    'data': {'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'},
                    'description': 'FL_HU_Program_1',
                    'event_catalogs': [
                        {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
                    ],
                    'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
                    'loss_type': 'LossGross',
                    'meta_data': {},
                    'modified': '2016-03-09T18:38:04.801820Z',
                    'profile': {
                        'attributes': {
                            'ModelID': ['1'],
                            'Peril': ['HU'],
                            'Region': ['US'],
                            'SubRegion': ['Florida']
                        },
                        'avg_annual_loss': 446831.486739948,
                        'currency': 'USD',
                        'max_loss': 8995286.82877091,
                        'min_loss': 10553.9672063884,
                        'non_zero_losses': 1000,
                        'num_losses': 1000
                    },
                    'status': 'processing_succeeded',
                    'status_message': None
                }
            ],
            'meta_data': {
                'business_unit': 'North America',
                'cat_modeler': 'Elizabeth Hawks',
                'client_id': 'Model A - Charlie Group Layer 1',
                'peril': 'EQ',
                'program_id': 3,
                'program_name': 'Charlie Group',
                'region': 'California',
                'underwriter': 'Travis Costa'
            },
            'modified': '2016-03-09T18:38:04.801820Z',
            'nth': 1,
            'participation': 0.092,
            'policy': None,
            'premium': {
                'currency': 'USD',
                'rate': None,
                'rate_currency': None,
                'value': 39939.9225,
                'value_date': None
            },
            'reinstatements': []
        },
        'target_currency': 'USD',
        'ylt_id': '99838575-6a3c-a7a2-d1e5-40a8e1b67b47'
    }

    analyzere_layer_view = convert_to_analyzere_object(layer_view_dict)

    return [
        '333bf15d-225a-a30c-b95d-22fff4722b5d',
        ['6a9bf278-4edc-4d28-b4bb-59f2283dbcb0'],
        analyzere_layer_view
    ]


@pytest.fixture(scope='session')
def loss_set():
    loss_set_dict = {
        '_type': 'ELTLossSet',
        'created': '2016-03-09T18:38:04.801820Z',
        'currency': 'USD',
        'data': {'ref_id': 'd99999e4-d66e-4c0a-a6ba-554a8598fea5'},
        'description': 'FL_HU_Program_1',
        'event_catalogs': [
            {'ref_id': 'aa8c316c-128c-485b-9144-5eed3f051c36'}
        ],
        'id': '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
        'loss_type': 'LossGross',
        'meta_data': {},
        'modified': '2016-03-09T18:38:04.801820Z',
        'profile': {
            'attributes': {
                'ModelID': ['1'],
                'Peril': ['HU'],
                'Region': ['US'],
                'SubRegion': ['Florida']
            },
            'avg_annual_loss': 446831.486739948,
            'currency': 'USD',
            'max_loss': 8995286.82877091,
            'min_loss': 10553.9672063884,
            'non_zero_losses': 1000,
            'num_losses': 1000
        },
        'status': 'processing_succeeded',
        'status_message': None
    }

    analyzere_loss_set = convert_to_analyzere_object(loss_set_dict)

    return [
        '6a9bf278-4edc-4d28-b4bb-59f2283dbcb0',
        analyzere_loss_set
    ]


@pytest.fixture(scope='session')
def portfolio_with_non_elt_loss_sets(portfolio):
    non_elt_portfolio = []
    non_elt_portfolio.append(portfolio[0])
    non_elt_portfolio.append(portfolio[1])
    non_elt_portfolio.append(portfolio[2])

    for i in range(0, len(non_elt_portfolio[2].layers)):
        for j in range(0, len(non_elt_portfolio[2].layers[i].loss_sets)):
            non_elt_portfolio[2].layers[i].loss_sets[j].type = 'YELTLossSet'

    return non_elt_portfolio


@pytest.fixture(scope='session')
def pv_with_p_with_non_elt_loss_sets(
        portfolio_view_with_portfolio):
    non_elt_portfolio_view = []
    non_elt_portfolio_view.append(portfolio_view_with_portfolio[0])
    non_elt_portfolio_view.append(portfolio_view_with_portfolio[1])
    non_elt_portfolio_view.append(portfolio_view_with_portfolio[2])

    for i in range(0, len(non_elt_portfolio_view[2].portfolio.layers)):
        for j in range(0, len(
                non_elt_portfolio_view[2].portfolio.layers[i].loss_sets)):
            non_elt_portfolio_view[2].portfolio.layers[i].loss_sets[j].type =\
                'YELTLossSet'

    return non_elt_portfolio_view


@pytest.fixture(scope='session')
def pv_with_lv_with_non_elt_loss_sets(
        portfolio_view_with_layer_views):
    non_elt_portfolio_view = []
    non_elt_portfolio_view.append(portfolio_view_with_layer_views[0])
    non_elt_portfolio_view.append(portfolio_view_with_layer_views[1])
    non_elt_portfolio_view.append(portfolio_view_with_layer_views[2])

    for i in range(0, len(non_elt_portfolio_view[2].layer_views)):
        for j in range(0, len(
                non_elt_portfolio_view[2].layer_views[i].layer.loss_sets)):
            non_elt_portfolio_view[2].layer_views[i].layer.loss_sets[j].type =\
                'YELTLossSet'

    return non_elt_portfolio_view


@pytest.fixture(scope='session')
def layer_with_non_elt_loss_sets(layer):
    non_elt_layer = []
    non_elt_layer.append(layer[0])
    non_elt_layer.append(layer[1])
    non_elt_layer.append(layer[2])

    for i in range(0, len(non_elt_layer[2].loss_sets)):
        non_elt_layer[2].loss_sets[i].type = 'YELTLossSet'

    return non_elt_layer


@pytest.fixture(scope='session')
def layer_view_with_non_elt_loss_sets(layer_view):
    non_elt_layer_view = []
    non_elt_layer_view.append(layer_view[0])
    non_elt_layer_view.append(layer_view[1])
    non_elt_layer_view.append(layer_view[2])

    for i in range(0, len(non_elt_layer_view[2].layer.loss_sets)):
        non_elt_layer_view[2].layer.loss_sets[i].type = 'YELTLossSet'

    return non_elt_layer_view


@pytest.fixture(scope='session')
def non_elt_loss_set(loss_set):
    non_elt_loss_set = []
    non_elt_loss_set.append(loss_set[0])
    non_elt_loss_set.append(loss_set[1])

    non_elt_loss_set[1].type = 'YELTLossSet'

    return non_elt_loss_set


@pytest.fixture(scope='session')
def elt_response_1():
    id = 'c054b33f-45df-4007-94f1-13d24935524d'
    elt_str_list = []
    elt_str_list.append('EventId,Loss')
    elt_str_list.append('1000,10.5')
    elt_str_list.append('1001,400.0')
    elt_str_list.append('1003,200.0')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_2():
    id = '11ace104-d814-4238-99ba-0a1a2faa4f2d'
    elt_str_list = []
    elt_str_list.append('EventId,Loss')
    elt_str_list.append('2100,20.25')
    elt_str_list.append('1000,600.0')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_3():
    id = '756f989c-1250-4149-97c1-9b57e3aa36b8'
    elt_str_list = []
    elt_str_list.append('EventId,Loss')
    elt_str_list.append('3000,10.5')
    elt_str_list.append('1003,1200.0')
    elt_str_list.append('3002,3000.1')
    elt_str_list.append('2100,3150.0')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_additional_columns_1():
    id = '97fcab1e-1afd-40ca-b439-5b0bab3cd576'
    elt_str_list = []
    elt_str_list.append('EventId,Loss,STDDEVI,STDDEVC,EXPVALUE')
    elt_str_list.append('02,100.5,4,5.7,99')
    elt_str_list.append('01,40.0,0.0,0,0.00')
    elt_str_list.append('3000,23300.0,4,5,234')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_additional_columns_2():
    id = 'c48bcda4-8ba5-4366-9c95-1904beb0d19e'
    elt_str_list = []
    elt_str_list.append('EventId,Loss,STDDEVI,STDDEVC,EXPVALUE')
    elt_str_list.append('03,20.250,4,5.6,0.01')
    elt_str_list.append('1000,600.00,0.01,0.04,0')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_additional_columns_3():
    id = '5489f16a-dbcf-42e6-a5c6-3b0ea05b293a'
    elt_str_list = []
    elt_str_list.append('EventId,Loss,STDDEVI,STDDEVC,EXPVALUE')
    elt_str_list.append('3000,105.5,0,0,0')
    elt_str_list.append('1420,120.0,1,1,1')
    elt_str_list.append('11420,30400.1,0.5,0.4,0.3')
    elt_str_list.append('02,3150.0,0.9,8.0,22')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_EventId():
    id = '0c7b46ac-3ae0-432e-931f-ae2c3f03481b'
    elt_str_list = []
    elt_str_list.append('EventId,Loss')
    elt_str_list.append('99000,1000000')
    elt_str_list.append('104000,2000000')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_EventID():
    id = '90c03895-ea84-4df6-81b4-b6582976004b'
    elt_str_list = []
    elt_str_list.append('EventID,Loss')
    elt_str_list.append('6454,4500.00')
    elt_str_list.append('6201,560.8')

    return [id, elt_str_list]


@pytest.fixture(scope='session')
def elt_response_dict(elt_response_EventId, elt_response_EventID):
    elt_response_dict = {}
    elt_response_dict['elt_response_EventId'] = elt_response_EventId
    elt_response_dict['elt_response_EventID'] = elt_response_EventID

    return elt_response_dict
