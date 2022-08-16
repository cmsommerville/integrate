import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefProvision, Model_RefDataTypes

def DATA_PROVISION_PRODUCT():
    return [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_provision_id': Model_RefProvision.find_one_by_attr({
            "ref_attr_code": "group_size"
        }).ref_id, 
        'config_provision_version_code': 'std_group_size',
        'config_provision_data_type_id': Model_RefDataTypes.find_one_by_attr({
            "ref_attr_code": "number"
        }).ref_id, 
        'config_provision_description': "This is the standard provision for CI21000 Group Size."
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_provision_id': Model_RefProvision.find_one_by_attr({
            "ref_attr_code": "sic_code"
        }).ref_id, 
        'config_provision_version_code': 'std_sic_code',
        'config_provision_data_type_id': Model_RefDataTypes.find_one_by_attr({
            "ref_attr_code": "string"
        }).ref_id, 
        'config_provision_description': "This is the standard provision for CI21000 SIC code."
    }, 
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/provision-product-list')
    res = requests.post(url, json=DATA_PROVISION_PRODUCT())
    if not res.ok: 
        raise Exception(res.text)