import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_ConfigBenefit, \
    Model_RefStates, Model_RefBenefit, Model_ConfigProductState


def _PRODUCT():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })



def BENEFITS(product: Model_ConfigProduct):
    return {
        "cancer": [state for state in product.states], 
        "heart_attack": [state for state in product.states], 
        "stroke": [state for state in product.states if state.config_product_state_id % 4 != 1], 
        "renal_failure": [state for state in product.states if state.config_product_state_id % 4 != 1], 
        "transplant": [state for state in product.states if state.config_product_state_id % 4 != 2], 
        "cis": [state for state in product.states if state.config_product_state_id % 4 != 3], 
        "cabg": [state for state in product.states if state.config_product_state_id % 4 != 0], 
        "ms": [state for state in product.states if state.config_product_state_id % 3 != 1], 
        "als": [state for state in product.states if state.config_product_state_id % 3 != 1], 
        "hsb": [state for state in product.states],
        "skin_cancer": [state for state in product.states if state.config_product_state_id % 4 != 1],  
    }


def DATA_BENEFIT_STATES(product):
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
    } for state in BENEFITS(product)['cancer']], 
    
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
    } for state in BENEFITS(product)['heart_attack']], 
    
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
    } for state in BENEFITS(product)['stroke']],
    
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
    } for state in BENEFITS(product)['renal_failure']],
    
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
    } for state in BENEFITS(product)['transplant']],
    
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
    } for state in BENEFITS(product)['cis']],
    
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
    } for state in BENEFITS(product)['cabg']],
    
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
    } for state in BENEFITS(product)['ms']],
    
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
    } for state in BENEFITS(product)['als']],
    
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
    } for state in BENEFITS(product)['hsb']],
    
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
    } for state in BENEFITS(product)['skin_cancer']],
]

def load(hostname: str, *args, **kwargs) -> None:
    product = _PRODUCT()
    url = urljoin(hostname, f'api/config/product/{product.config_product_id}/benefit/states')
    res = requests.post(url, json=DATA_BENEFIT_STATES(product))
    if not res.ok: 
        raise Exception(res.text)