import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_ConfigProvision, \
    Model_RefStates, Model_RefProvision


_PRODUCT = Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

PROVISIONS = {
    "group_size": [state for state in _PRODUCT.states], 
    "sic_code": [state for state in _PRODUCT.states if state.config_product_state_id % 4 != 1], 
}


DATA_PROVISION_STATES = [
    *[{
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }), 
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_provision_state_effective_date': state.config_product_state_effective_date, 
        'config_provision_state_expiration_date': state.config_product_state_expiration_date, 
    } for state in PROVISIONS['group_size']], 
    
    *[{
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "sic_code"
            }).ref_id
        }), 
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_provision_state_effective_date': state.config_product_state_effective_date, 
        'config_provision_state_expiration_date': state.config_product_state_expiration_date, 
    } for state in PROVISIONS['group_size']], 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProvisionState_List'), DATA_PROVISION_STATES)


if __name__ == '__main__':
    load()