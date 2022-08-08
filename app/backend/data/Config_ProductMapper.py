import requests
from flask_restx import fields
from ..models import Model_ConfigProduct, Model_RefAttrMapperType, Model_ConfigAttributeDetail

_PRODUCT_ID = Model_ConfigProduct.find_one_by_attr({
      "product_code": "CI"
  })

_COMPOSITE = Model_RefAttrMapperType.find_one_by_attr({
      "ref_attr_code": "composite"
  })
_DISTINCT = Model_RefAttrMapperType.find_one_by_attr({
      "ref_attr_code": "composite"
  })

DATA_PRODUCT_MAPPER__GENDER = [
    { 
        'config_product_id': _PRODUCT_ID.config_product_id,
        'config_attr_type_code': 'gender', 
        'config_attr_mapper_type_id': _COMPOSITE.ref_id, 
        'is_default': True, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'M'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'X'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'F'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'X'
                    }).config_attr_detail_id
            }
        ]
    }, 
    { 
        'config_product_id': _PRODUCT_ID.config_product_id,
        'config_attr_type_code': 'gender', 
        'config_attr_mapper_type_id': _DISTINCT.ref_id, 
        'is_default': False, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'M'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'M'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'F'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'F'
                    }).config_attr_detail_id
            }
        ]
    }
]






DATA_PRODUCT_MAPPER__SMOKER_STATUS = [
    { 
        'config_product_id': _PRODUCT_ID.config_product_id,
        'config_attr_type_code': 'smoker_status', 
        'config_attr_mapper_type_id': _COMPOSITE.ref_id, 
        'is_default': False, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'N'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'U'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'T'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'U'
                    }).config_attr_detail_id
            }
        ]
    }, 
    { 
        'config_product_id': _PRODUCT_ID.config_product_id,
        'config_attr_type_code': 'smoker_status', 
        'config_attr_mapper_type_id': _DISTINCT.ref_id, 
        'is_default': True, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'N'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'N'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'T'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'T'
                    }).config_attr_detail_id
            }
        ]
    }
]



def load() -> None:
    requests.post(fields.Url('CRUD_ConfigProductMapperSet_Gender_List'), DATA_PRODUCT_MAPPER__GENDER)
    requests.post(fields.Url('CRUD_ConfigProductMapperSet_SmokerStatus_List'), DATA_PRODUCT_MAPPER__SMOKER_STATUS)


if __name__ == '__main__':
    load()