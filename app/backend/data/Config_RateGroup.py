import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct

DATA_RATE_GROUP = [
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


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigCoverage_List'), DATA_RATE_GROUP)


if __name__ == '__main__':
    load()