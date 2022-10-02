import requests
from requests.compat import urljoin

DATA_GENDER = [
    {
        'config_attr_type_code': 'gender', 
        'config_attr_set_label': 'Standard M/F/X', 
        'attributes': [
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
        'attributes': [
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
        'attributes': [
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
    }, 
    {
        'config_attr_type_code': 'relationship', 
        'config_attr_set_label': 'Standard Four Tier', 
        'attributes': [
            {
                'config_attr_detail_code': 'EE_ONLY',
                'config_attr_detail_label': 'Employee',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'EE_SP',
                'config_attr_detail_label': 'Employee + Spouse',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'EE_CH',
                'config_attr_detail_label': 'Employee + Children',
                'is_composite_id': False
            }, 
            {
                'config_attr_detail_code': 'FAM',
                'config_attr_detail_label': 'Family',
                'is_composite_id': False
            }, 
        ]
    }
]


DATA_NO_JOINS = [
    {
        'config_attr_set_id': -1, 
        'config_attr_type_code': '__nojoin__', 
        'config_attr_set_label': 'No Join', 
        'attributes': [
            {
                'config_attr_detail_id': -1, 
                'config_attr_detail_code': '',
                'config_attr_detail_label': '',
                'is_composite_id': False
            }, 
        ]
    }, 
]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/config/attribute-set-gender-list')
    res = requests.post(url, json=DATA_GENDER)
    if not res.ok: 
        raise Exception(res.text)
    url = urljoin(hostname, 'api/crud/config/attribute-set-smoker-status-list')
    res = requests.post(url, json=DATA_SMOKER_STATUS)
    if not res.ok: 
        raise Exception(res.text)
    url = urljoin(hostname, 'api/crud/config/attribute-set-relationship-list')
    res = requests.post(url, json=DATA_RELATIONSHIP)
    if not res.ok: 
        raise Exception(res.text)
    url = urljoin(hostname, 'api/crud/config/attribute-set-list')
    res = requests.post(url, json=DATA_NO_JOINS)
    if not res.ok: 
        raise Exception(res.text)