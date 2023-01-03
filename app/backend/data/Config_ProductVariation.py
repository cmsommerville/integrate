import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefProductVariation

def PRODUCT_ID(): 
    return Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id

def DATA_PRODUCT_VARIATION(product_id: int):
    return [
    {
        'config_product_id': product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'issue_age',
        }).ref_id, 
        'config_product_variation_version_code': 'std_issue_age', 
    }, 
    {
        'config_product_id': product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'attained_age',
        }).ref_id, 
        'config_product_variation_version_code': 'std_attained_age', 
    }, 
]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f'api/config/product/{product_id}/variations')
    res = requests.post(url, json=DATA_PRODUCT_VARIATION(product_id))
    if not res.ok: 
        raise Exception(res.text)