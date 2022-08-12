import requests
from requests.compat import urljoin
from  ..models import Model_RefProvision, Model_ConfigProvision, Model_RefComparisonOperator, \
    Model_RefDataTypes

def DATA_FACTOR(): 
    return [
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }).config_provision_id, 
        'factor_priority': 1, 
        'factor_value': 1.0, 
        'factor_rules': [
            {
                'comparison_class_name': 'Model_SelectionProvision',
                'comparison_column_name': 'selection_provision_value',
                'comparison_operator_id': Model_RefComparisonOperator.find_one_by_attr({
                    "ref_attr_symbol": "<"
                }).ref_id,
                'comparison_column_value': '1000',
                'comparison_column_data_type_id': Model_RefDataTypes.find_one_by_attr({
                    'ref_attr_code': 'number'
                }).ref_id,
            },
        ]
    }, 
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }).config_provision_id, 
        'factor_priority': 1, 
        'factor_value': 0.9, 
        'factor_rules': [
            {
                'comparison_class_name': 'Model_SelectionProvision',
                'comparison_column_name': 'selection_provision_value',
                'comparison_operator_id': Model_RefComparisonOperator.find_one_by_attr({
                    "ref_attr_symbol": "<"
                }).ref_id,
                'comparison_column_value': '5000',
                'comparison_column_data_type_id': Model_RefDataTypes.find_one_by_attr({
                    'ref_attr_code': 'number'
                }).ref_id,
            },
        ]
    }, 
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }).config_provision_id, 
        'factor_priority': 1, 
        'factor_value': 0.8, 
        'factor_rules': [
            {
                'comparison_class_name': 'Model_SelectionProvision',
                'comparison_column_name': 'selection_provision_value',
                'comparison_operator_id': Model_RefComparisonOperator.find_one_by_attr({
                    "ref_attr_symbol": ">="
                }).ref_id,
                'comparison_column_value': '5000',
                'comparison_column_data_type_id': Model_RefDataTypes.find_one_by_attr({
                    'ref_attr_code': 'number'
                }).ref_id,
            },
        ]
    }, 

    
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "sic_code"
            }).ref_id
        }).config_provision_id, 
        'factor_priority': 1, 
        'factor_value': 0.82, 
        'factor_rules': [
            {
                'comparison_class_name': 'Model_SelectionProvision',
                'comparison_column_name': 'selection_provision_value',
                'comparison_operator_id': Model_RefComparisonOperator.find_one_by_attr({
                    "ref_attr_symbol": "<"
                }).ref_id,
                'comparison_column_value': '5000',
                'comparison_column_data_type_id': Model_RefDataTypes.find_one_by_attr({
                    'ref_attr_code': 'string'
                }).ref_id,
            },
        ]
    }, 
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "sic_code"
            }).ref_id
        }).config_provision_id, 
        'factor_priority': 1, 
        'factor_value': 1.07, 
        'factor_rules': [
            {
                'comparison_class_name': 'Model_SelectionProvision',
                'comparison_column_name': 'selection_provision_value',
                'comparison_operator_id': Model_RefComparisonOperator.find_one_by_attr({
                    "ref_attr_symbol": ">="
                }).ref_id,
                'comparison_column_value': '5000',
                'comparison_column_data_type_id': Model_RefDataTypes.find_one_by_attr({
                    'ref_attr_code': 'string'
                }).ref_id,
            },
        ]
    }, 
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/factor-list')
    res = requests.post(url, json=DATA_FACTOR())
    if not res.ok: 
        raise Exception(res.text)