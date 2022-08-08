import requests
from flask_restx import fields
from ..models import Model_ConfigAttributeDetail


DATA_GENDER_DIST = [
    {
        'config_attr_type_code': 'gender', 
        'config_attr_distribution_set_label': 'Male/Female 50/50', 
        'gender_distribution': [
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'M'
                }), 
                'weight': 50
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'F'
                }), 
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
                }), 
                'weight': 40
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'F'
                }), 
                'weight': 60
            }, 
        ]
    }
]


DATA_SMOKER_DIST = [
    {
        'config_attr_type_code': 'smoker_status', 
        'config_attr_distribution_set_label': 'N/T 85/15', 
        'smoker_status_distribution': [
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'N'
                }), 
                'weight': 85
            }, 
            {
                'config_attr_detail_id': Model_ConfigAttributeDetail.find_one_by_attr({
                    'config_attr_detail_code': 'T'
                }), 
                'weight': 15
            }, 
        ]
    }
]

def load() -> None:
    requests.post(fields.Url('Config_AttributeDistributionSet_Gender_List'), DATA_GENDER_DIST)
    requests.post(fields.Url('Config_AttributeDistributionSet_SmokerStatus_List'), DATA_SMOKER_DIST)


if __name__ == '__main__':
    load()