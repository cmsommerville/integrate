import requests
from requests.compat import urljoin
from itertools import product
from  ..models import Model_ConfigProductVariation, Model_ConfigBenefit

def VARIATIONS():
    return Model_ConfigProductVariation.find_all()

def BENEFITS():
    return Model_ConfigBenefit.find_all()


def DATA_BENEFIT_VARIATIONS():
    data = []
    for pv, bnft in product(VARIATIONS(), BENEFITS()):
        data.append({
            'config_benefit_id': bnft.config_benefit_id, 
            'config_product_variation_id': pv.config_product_variation_id, 
            'is_enabled': True
        })
    return data
    

def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/benefit-product-variation-list')
    res = requests.post(url, json=DATA_BENEFIT_VARIATIONS())
    if not res.ok: 
        raise Exception(res.text)