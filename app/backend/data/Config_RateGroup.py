import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct

def DATA_RATE_GROUP(): 
    return [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_rate_group_code': 'APU', 
        'config_rate_group_label': "Annual Rate per $1000", 
        'unit_value': 1000, 
        'apply_discretionary_factor': True
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'config_rate_group_code': 'FLAT', 
        'config_rate_group_label': "Flat Rate", 
        'unit_value': 1, 
        'apply_discretionary_factor': False
    }, 
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/rate-group-list')
    res = requests.post(url, json=DATA_RATE_GROUP())
    if not res.ok: 
        raise Exception(res.text)