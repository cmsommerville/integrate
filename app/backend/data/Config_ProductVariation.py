import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefProductVariation

def DATA_PRODUCT_VARIATION():
    return [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'issue_age',
        }).ref_id, 
        'config_product_variation_version_code': 'std_issue_age', 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'attained_age',
        }).ref_id, 
        'config_product_variation_version_code': 'std_attained_age', 
    }, 
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/product-variation-list')
    res = requests.post(url, json=DATA_PRODUCT_VARIATION())
    if not res.ok: 
        raise Exception(res.text)