import requests
from flask_restx import fields
from  ..models import Model_ConfigProvision, Model_ConfigProvisionUI_Input, Model_ConfigProvisionUI_Checkbox, \
    Model_ConfigProvisionUI_Select, Model_ConfigProvisionUI_SelectItem, Model_RefProvision, \
    Model_RefInputTypes

DATA_PROVISION_UI = [
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }), 
        'component_type_code': 'INPUT', 
        "input_type_id": Model_RefInputTypes.find_one_by_attr({
            "ref_attr_code": "number"
        }).ref_id, 
        'min_value': 0, 
        'max_value': 999999, 
        'step_value': 1, 
        'placeholder': 'A number between 0 - 999,999', 
    }, 
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "sic_code"
            }).ref_id
        }), 
        'component_type_code': 'INPUT', 
        "input_type_id": Model_RefInputTypes.find_one_by_attr({
            "ref_attr_code": "text"
        }).ref_id, 
        'min_length': 4, 
        'max_length': 4, 
        'placeholder': 'Enter the 4 digit SIC Code', 
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProvisionUI_List'), DATA_PROVISION_UI)


if __name__ == '__main__':
    load()