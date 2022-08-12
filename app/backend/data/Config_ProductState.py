import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefStates

def DATA_PRODUCT_STATES():
    return [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "AK"
        }).state_id, 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "AL"
        }).state_id, 
        'config_product_state_effective_date': '2023-01-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "SC"
        }).state_id, 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "NC"
        }).state_id, 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '2022-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "TX"
        }).state_id, 
        'config_product_state_effective_date': '2020-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': Model_RefStates.find_one_by_attr({
            "state_code": "GA"
        }).state_id, 
        'config_product_state_effective_date': '2022-12-01', 
        'config_product_state_expiration_date': '9999-12-31', 
    }, 
]

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/product-state-list')
    res = requests.post(url, json=DATA_PRODUCT_STATES())
    if not res.ok: 
        raise Exception(res.text)