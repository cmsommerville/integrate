import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_ConfigCoverage

DATA_COVERAGE = [
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


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigCoverage_List'), DATA_COVERAGE)


if __name__ == '__main__':
    load()