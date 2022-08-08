import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_RefStates

DATA_PRODUCT_STATES = [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "AK"
        }), 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "AL"
        }), 
        'config_product_state_effective_date': '2023-01-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "SC"
        }), 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "NC"
        }), 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '2022-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "TX"
        }), 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "GA"
        }), 
        'config_product_state_effective_date': '2022-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProductState_List'), DATA_PRODUCT_STATES)


if __name__ == '__main__':
    load()