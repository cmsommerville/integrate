import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_ConfigBenefit, \
    Model_RefStates, Model_RefBenefit, Model_ConfigProductState


def _PRODUCT():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })



def BENEFITS():
    return {
        "cancer": [state for state in _PRODUCT().states], 
        "heart_attack": [state for state in _PRODUCT().states], 
        "stroke": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 1], 
        "renal_failure": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 1], 
        "transplant": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 2], 
        "cis": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 3], 
        "cabg": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 0], 
        "ms": [state for state in _PRODUCT().states if state.config_product_state_id % 3 != 1], 
        "als": [state for state in _PRODUCT().states if state.config_product_state_id % 3 != 1], 
        "hsb": [state for state in _PRODUCT().states],
        "skin_cancer": [state for state in _PRODUCT().states if state.config_product_state_id % 4 != 1],  
    }


def DATA_BENEFIT_STATES():
    return [
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "cancer"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cancer"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['cancer']], 
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "heart_attack"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "heart_attack"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['heart_attack']], 
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "stroke"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "stroke"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['stroke']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "renal_failure"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "renal_failure"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['renal_failure']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "transplant"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "transplant"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['transplant']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "cis"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cis"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['cis']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "cabg"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cabg"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['cabg']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "ms"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "ms"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['ms']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "als"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "als"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['als']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "hsb"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "hsb"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['hsb']],
    
    *[{
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "skin_cancer"
            }).ref_id
        }).config_benefit_id, 
        "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "skin_cancer"
        }).ref_id,
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'state_id': state.state_id, 
        'config_benefit_state_effective_date': str(state.config_product_state_effective_date), 
        'config_benefit_state_expiration_date': str(state.config_product_state_expiration_date), 
    } for state in BENEFITS()['skin_cancer']],
]

def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/benefit-state-list')
    res = requests.post(url, json=DATA_BENEFIT_STATES())
    if not res.ok: 
        raise Exception(res.text)