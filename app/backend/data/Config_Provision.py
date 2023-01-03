import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefProvision, Model_RefDataTypes

def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    }).config_product_id

def DATA_PROVISION_PRODUCT(product_id: int):
    return [
    {
        'config_product_id': product_id, 
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
        'config_product_id': product_id, 
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

def DATA_PROVISION_RATE_TABLE(product_id: int):
    return [
        {
            'config_product_id': product_id, 
            'ref_provision_id': Model_RefProvision.find_one_by_attr({
                "ref_attr_code": "reduction_at_70"
            }).ref_id, 
            'config_provision_version_code': 'std_reduction_at_70',
            'config_provision_data_type_id': Model_RefDataTypes.find_one_by_attr({
                "ref_attr_code": "boolean"
            }).ref_id, 
            'config_provision_description': "This is the standard provision for CI21000 Reduction at Age 70."
        }, 
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f'api/config/product/{product_id}/provisions/prd')
    res = requests.post(url, json=DATA_PROVISION_PRODUCT(product_id))
    if not res.ok: 
        raise Exception(res.text)
    url = urljoin(hostname, f'api/config/product/{product_id}/provisions/rt')
    res = requests.post(url, json=DATA_PROVISION_RATE_TABLE(product_id))
    if not res.ok: 
        raise Exception(res.text)