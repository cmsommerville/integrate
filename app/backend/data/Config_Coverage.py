import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_ConfigCoverage

def DATA_COVERAGE(): 
    return [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_coverage_code': 'base', 
        'config_coverage_label': "Base Benefits"
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_coverage_code': 'heart_rider', 
        'config_coverage_label': "Heart Rider"
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_coverage_code': 'prog_benefits', 
        'config_coverage_label': "Progressive Disease Rider"
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_coverage_code': 'opt_benefits', 
        'config_coverage_label': "Optional Benefits"
    }, 
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/coverage-list')
    res = requests.post(url, json=DATA_COVERAGE())
    if not res.ok: 
        raise Exception(res.text)