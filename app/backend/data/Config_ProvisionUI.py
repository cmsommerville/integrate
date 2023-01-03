import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProvision, Model_ConfigProduct, Model_RefProvision, Model_RefInputTypes

def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    }).config_product_id

def DATA_PROVISION_UI(): 
    return [
    {
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }).config_provision_id, 
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
        }).config_provision_id, 
        'component_type_code': 'INPUT', 
        "input_type_id": Model_RefInputTypes.find_one_by_attr({
            "ref_attr_code": "text"
        }).ref_id, 
        'min_length': 4, 
        'max_length': 4, 
        'placeholder': 'Enter the 4 digit SIC Code', 
    }, 
]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f'api/config/product/{product_id}/provision/ui-components')
    res = requests.post(url, json=DATA_PROVISION_UI())
    if not res.ok: 
        raise Exception(res.text)