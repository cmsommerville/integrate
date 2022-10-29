import requests
from requests.compat import urljoin
from  ..models import Model_ConfigRateGroup, Model_ConfigAttributeDetail

def DATA_FACE_AMOUNTS(): 
    return {
        'vary_by_gender': False, 
        'vary_by_smoker_status': False, 
        'vary_by_relationship': True, 
        'face_amounts': [
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 5000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 10000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 15000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 20000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 25000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 30000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 35000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 40000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 45000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'EE'
                }).config_attr_detail_id, 
                'face_amount_value': 50000, 
            }, 



            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 5000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 7500, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 10000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 12500, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 15000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 17500, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 20000, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 22500, 
            }, 
            {
                'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
                    "config_rate_group_code": "APU"
                }).config_rate_group_id, 
                'config_relationship_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'SP'
                }).config_attr_detail_id, 
                'face_amount_value': 25000, 
            }, 
        ]
    }


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/rate-group-face-amounts-list')
    res = requests.post(url, json=DATA_FACE_AMOUNTS())
    if not res.ok: 
        raise Exception(res.text)