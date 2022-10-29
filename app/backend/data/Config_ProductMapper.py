import requests
from requests.compat import urljoin
from ..models import Model_ConfigProduct, Model_RefAttrMapperType, Model_ConfigAttributeDetail

def _PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

def _COMPOSITE(): 
    return Model_RefAttrMapperType.find_one_by_attr({
        "ref_attr_code": "composite"
    })
def _DISTINCT(): 
    return Model_RefAttrMapperType.find_one_by_attr({
        "ref_attr_code": "distinct"
    })

def DATA_PRODUCT_MAPPER__GENDER(): 
    return [
    { 
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_attr_type_code': 'gender', 
        'config_attr_mapper_type_id': _COMPOSITE().ref_id, 
        'is_default': True, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'X'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'X'
                    }).config_attr_detail_id
            }, 
        ]
    }, 
    { 
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_attr_type_code': 'gender', 
        'config_attr_mapper_type_id': _DISTINCT().ref_id, 
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



def DATA_PRODUCT_MAPPER__SMOKER_STATUS(): 
    return [
    { 
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_attr_type_code': 'smoker_status', 
        'config_attr_mapper_type_id': _COMPOSITE().ref_id, 
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
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_attr_type_code': 'smoker_status', 
        'config_attr_mapper_type_id': _DISTINCT().ref_id, 
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



def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/product-mapper-set-gender-list')
    res = requests.post(url, json=DATA_PRODUCT_MAPPER__GENDER())
    if not res.ok: 
        raise Exception(res.text)

    url = urljoin(hostname, 'api/crud/config/product-mapper-set-smoker-status-list')
    res = requests.post(url, json=DATA_PRODUCT_MAPPER__SMOKER_STATUS())
    if not res.ok: 
        raise Exception(res.text)