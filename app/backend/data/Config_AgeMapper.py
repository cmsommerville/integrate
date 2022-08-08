import requests
from flask_restx import fields
from ..models import Model_ConfigProduct

_PRODUCT_ID = Model_ConfigProduct.find_one_by_attr({
      "product_code": "CI"
  })

DATA_AGE_MAPPER = [
    { 'from_age_value': 18, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 19, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 20, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 21, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 22, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 23, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 24, 'to_age_value': 22, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 25, 'to_age_value': 27, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 26, 'to_age_value': 27, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 27, 'to_age_value': 27, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 28, 'to_age_value': 27, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 29, 'to_age_value': 27, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 30, 'to_age_value': 32, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 31, 'to_age_value': 32, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 32, 'to_age_value': 32, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 33, 'to_age_value': 32, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 34, 'to_age_value': 32, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 35, 'to_age_value': 37, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 36, 'to_age_value': 37, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 37, 'to_age_value': 37, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 38, 'to_age_value': 37, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 39, 'to_age_value': 37, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 40, 'to_age_value': 42, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 41, 'to_age_value': 42, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 42, 'to_age_value': 42, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 43, 'to_age_value': 42, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 44, 'to_age_value': 42, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 45, 'to_age_value': 47, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 46, 'to_age_value': 47, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 47, 'to_age_value': 47, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 48, 'to_age_value': 47, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 49, 'to_age_value': 47, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 50, 'to_age_value': 52, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 51, 'to_age_value': 52, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 52, 'to_age_value': 52, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 53, 'to_age_value': 52, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 54, 'to_age_value': 52, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 55, 'to_age_value': 57, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 56, 'to_age_value': 57, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 57, 'to_age_value': 57, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 58, 'to_age_value': 57, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 59, 'to_age_value': 57, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 60, 'to_age_value': 62, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 61, 'to_age_value': 62, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 62, 'to_age_value': 62, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 63, 'to_age_value': 62, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 64, 'to_age_value': 62, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 65, 'to_age_value': 67, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 66, 'to_age_value': 67, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 67, 'to_age_value': 67, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 68, 'to_age_value': 67, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 69, 'to_age_value': 67, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 70, 'to_age_value': 72, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 71, 'to_age_value': 72, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 72, 'to_age_value': 72, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 73, 'to_age_value': 72, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 74, 'to_age_value': 72, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 75, 'to_age_value': 77, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 76, 'to_age_value': 77, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 77, 'to_age_value': 77, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 78, 'to_age_value': 77, "config_product_id":  _PRODUCT_ID},
    { 'from_age_value': 79, 'to_age_value': 77, "config_product_id":  _PRODUCT_ID},
  ]


def load() -> None:
    requests.post(fields.Url('Config_AgeMapperDetail_List'), DATA_AGE_MAPPER)


if __name__ == '__main__':
    load()