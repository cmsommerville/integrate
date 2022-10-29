import requests
from requests.compat import urljoin
from ..models import Model_ConfigProduct, Model_RefAttrMapperType, Model_ConfigAttributeDetail

def _PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

def DATA_RELATIONSHIP_MAPPER(): 
    return [
    { 
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_relationship_mapper_set_code': 'standard', 
        'config_relationship_mapper_set_label': "Standard gender distinct premiums", 
        'is_default': True, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'SP'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'SP'
                    }).config_attr_detail_id
            }
        ]
    }, 
    { 
        'config_product_id': _PRODUCT_ID().config_product_id,
        'config_relationship_mapper_set_code': 'family_four_tier', 
        'config_relationship_mapper_set_label': "Family Four Tier Premiums", 
        'is_default': False, 
        'mappers': [
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE_ONLY'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE_SP'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'SP'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE_SP'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE_CH'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'CH'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE_CH'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'EE'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'FAM'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'SP'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'FAM'
                    }).config_attr_detail_id
            }, 
            {
                'from_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'CH'
                    }).config_attr_detail_id, 
                'to_config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                        "config_attr_detail_code": 'FAM'
                    }).config_attr_detail_id
            }
        ]
    }, 
]





def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/relationship-mapper-set-list')
    res = requests.post(url, json=DATA_RELATIONSHIP_MAPPER())
    if not res.ok: 
        raise Exception(res.text)
