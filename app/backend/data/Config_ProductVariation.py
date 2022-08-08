import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_RefProductVariation

DATA_PRODUCT_VARIATION = [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'issue_age',
        }).ref_id
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_product_variation_id': Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": 'attained_age',
        }).ref_id
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProductVariation_List'), DATA_PRODUCT_VARIATION)


if __name__ == '__main__':
    load()