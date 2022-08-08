import requests
from flask_restx import fields
from  ..models import Model_RefProvision, Model_ConfigProvision, Model_RefComparisonOperator, \
    Model_RefDataTypes

DATA_FACTOR = [
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
                'comparison_column_data_type_id': 'number',
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
                'comparison_column_data_type_id': 'number',
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
                'comparison_column_data_type_id': 'number',
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
                'comparison_column_data_type_id': 'string',
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
                'comparison_column_data_type_id': 'string',
            },
        ]
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProvision_Product_List'), DATA_FACTOR)


if __name__ == '__main__':
    load()