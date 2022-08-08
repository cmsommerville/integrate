import requests
from flask_restx import fields

DATA_GENDER = [
    {
        'config_attr_type_code': 'gender', 
        'config_attr_set_label': 'Standard M/F/X', 
        'genders': [
            {
                'config_attr_detail_code': 'M',
                'config_attr_detail_label': 'Male',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'F',
                'config_attr_detail_label': 'Female',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'X',
                'config_attr_detail_label': 'Composite',
                'is_composite_id': True
            }, 
        ]
    }
]


DATA_SMOKER_STATUS = [
    {
        'config_attr_type_code': 'smoker_status', 
        'config_attr_set_label': 'Standard N/T/U', 
        'smoker_statuses': [
            {
                'config_attr_detail_code': 'N',
                'config_attr_detail_label': 'Non-Tobacco',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'T',
                'config_attr_detail_label': 'Tobacco',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'U',
                'config_attr_detail_label': 'Composite',
                'is_composite_id': True
            }, 
        ]
    }
]



DATA_RELATIONSHIP = [
    {
        'config_attr_type_code': 'relationship', 
        'config_attr_set_label': 'Standard EE/SP/CH', 
        'relationships': [
            {
                'config_attr_detail_code': 'EE',
                'config_attr_detail_label': 'Employee',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'SP',
                'config_attr_detail_label': 'Spouse',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'CH',
                'config_attr_detail_label': 'Children',
                'is_composite_id': False
            }, 
        ]
    }
]



def load() -> None:
    requests.post(fields.Url('Config_AttributeSet_Gender_List'), DATA_GENDER)
    requests.post(fields.Url('Config_AttributeSet_SmokerStatus_List'), DATA_SMOKER_STATUS)
    requests.post(fields.Url('Config_AttributeSet_Relationship_List'), DATA_RELATIONSHIP)


if __name__ == '__main__':
    load()