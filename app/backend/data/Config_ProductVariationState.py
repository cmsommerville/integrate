import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_ConfigProductVariation, \
    Model_RefStates, Model_ConfigAgeBandSet, Model_RefProductVariation


def _PRODUCT():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

def _VARIATIONS(product: Model_ConfigProduct):
    return {
        "issue_age": [state for state in product.states], 
        "attained_age": [state for state in product.states if state.config_product_state_id % 4 != 1] 
    }

def DATA_PRODUCT_VARIATION_STATE(product: Model_ConfigProduct):
    return [
     *[{
        'config_product_id': product.config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'issue_age',
        }).ref_id, 
        'state_id': state.state_id, 
        'config_product_variation_id': Model_ConfigProductVariation.find_one_by_attr({
            'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
                "ref_attr_code": 'issue_age',
            }).ref_id, 
        }).config_product_variation_id, 
        'config_product_variation_state_effective_date': str(state.config_product_state_effective_date), 
        'config_product_variation_state_expiration_date': str(state.config_product_state_expiration_date), 
        'config_age_band_set_id': Model_ConfigAgeBandSet.find_one_by_attr({
            "config_age_band_set_label": "Standard 10 Year Age Bands"
        }).config_age_band_set_id
    } for state in _VARIATIONS(product)['issue_age']], 

     *[{
        'config_product_id': product.config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'attained_age',
        }).ref_id, 
        'state_id': state.state_id, 
        'config_product_variation_id': Model_ConfigProductVariation.find_one_by_attr({
            'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
                "ref_attr_code": 'attained_age',
            }).ref_id, 
        }).config_product_variation_id, 
        'config_product_variation_state_effective_date': str(state.config_product_state_effective_date), 
        'config_product_variation_state_expiration_date': str(state.config_product_state_expiration_date), 
        'config_age_band_set_id': Model_ConfigAgeBandSet.find_one_by_attr({
            "config_age_band_set_label": "Standard 5 Year Age Bands"
        }).config_age_band_set_id
    } for state in _VARIATIONS(product)['attained_age']], 
]



def load(hostname: str, *args, **kwargs) -> None:
    product = _PRODUCT()
    url = urljoin(hostname, f'api/config/product/{product.config_product_id}/variation/states')
    res = requests.post(url, json=DATA_PRODUCT_VARIATION_STATE(product))
    if not res.ok: 
        raise Exception(res.text)