import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_RefProvision

DATA_PROVISION_PRODUCT = [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_provision_id': Model_RefProvision.find_one_by_attr({
            "ref_attr_code": "group_size"
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
        'config_provision_description': "This is the standard provision for CI21000 SIC code."
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProvision_Product_List'), DATA_PROVISION_PRODUCT)


if __name__ == '__main__':
    load()