import requests
from requests.compat import urljoin
from ..models import Model_ConfigAttributeDetail


def DATA_GENDER_DIST():
    return [
    {
        'config_attr_type_code': 'gender', 
        'config_attr_distribution_set_label': 'Male/Female 50/50', 
        'gender_distribution': [
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'M'
                }).config_attr_detail_id, 
                'weight': 50
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'F'
                }).config_attr_detail_id, 
                'weight': 50
            }, 
        ]
    }, 
    {
        'config_attr_type_code': 'gender', 
        'config_attr_distribution_set_label': 'Male/Female 40/60', 
        'gender_distribution': [
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'M'
                }).config_attr_detail_id, 
                'weight': 40
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'F'
                }).config_attr_detail_id, 
                'weight': 60
            }, 
        ]
    }
]


def DATA_SMOKER_DIST():
    return [
    {
        'config_attr_type_code': 'smoker_status', 
        'config_attr_distribution_set_label': 'N/T 85/15', 
        'smoker_status_distribution': [
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'N'
                }).config_attr_detail_id, 
                'weight': 85
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'T'
                }).config_attr_detail_id, 
                'weight': 15
            }, 
        ]
    }
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/attribute-distribution-set-gender-list')
    res = requests.post(url, json=DATA_GENDER_DIST())
    if not res.ok: 
        raise Exception(res.text)

    url = urljoin(hostname, 'api/crud/config/attribute-distribution-set-smoker-status-list')
    res = requests.post(url, json=DATA_SMOKER_DIST())
    if not res.ok: 
        raise Exception(res.text)