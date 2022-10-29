import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_ConfigProvision, \
    Model_RefStates, Model_RefProvision


def _PRODUCT():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

def PROVISIONS():
    return {
        "group_size": [state for state in _PRODUCT().states], 
        "sic_code": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 1], 
    }


def DATA_PROVISION_STATES(): 
    return [
    *[{
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "group_size"
            }).ref_id
        }).config_provision_id, 
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        "ref_provision_id": Model_RefProvision.find_one_by_attr({
            "ref_attr_code": "group_size"
        }).ref_id, 
        'state_id': state.state_id, 
        'config_provision_state_effective_date': str(state.config_product_state_effective_date), 
        'config_provision_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in PROVISIONS()['group_size']], 
    
    *[{
        'config_provision_id': Model_ConfigProvision.find_one_by_attr({
            "ref_provision_id": Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "sic_code"
            }).ref_id
        }).config_provision_id, 
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        "ref_provision_id": Model_RefProvision.find_one_by_attr({
            "ref_attr_code": "sic_code"
        }).ref_id, 
        'state_id': state.state_id, 
        'config_provision_state_effective_date': str(state.config_product_state_effective_date), 
        'config_provision_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in PROVISIONS()['sic_code']], 
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/provision-state-list')
    res = requests.post(url, json=DATA_PROVISION_STATES())
    if not res.ok: 
        raise Exception(res.text)