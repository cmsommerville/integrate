import requests
import json
from requests.compat import urljoin
from  ..models import Model_ConfigBenefit, Model_RefBenefit

def BENEFIT_ID(): 
    return Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "skin_cancer"
            }).ref_id
        }).config_benefit_id

def DATA_BENEFIT_DURATION(benefit_id: int):
    return [
    {
        'config_benefit_id': benefit_id, 
        'config_benefit_duration_set_code': 'annual_payments', 
        'config_benefit_duration_set_label': "Number of Payments per Year", 
        "duration_items": [
            {
                "config_benefit_duration_detail_code": "1", 
                "config_benefit_duration_detail_label": "1 per year", 
                "config_benefit_duration_factor": 0.85, 
                "acl": [
                    {
                        'auth_role_code': 'uw900'
                    }, 
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
            {
                "config_benefit_duration_detail_code": "2", 
                "config_benefit_duration_detail_label": "2 per year", 
                "config_benefit_duration_factor": 0.95, 
                "acl": [
                    {
                        'auth_role_code': 'uw900'
                    }, 
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
            {
                "config_benefit_duration_detail_code": "3", 
                "config_benefit_duration_detail_label": "3 per year", 
                "config_benefit_duration_factor": 1, 
                "acl": [
                    {
                        'auth_role_code': 'uw900'
                    }, 
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
            {
                "config_benefit_duration_detail_code": "4", 
                "config_benefit_duration_detail_label": "4 per year", 
                "config_benefit_duration_factor": 1.1, 
                "acl": [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ]
    }, 
]



def load(hostname: str, *args, **kwargs) -> None:
    benefit_id = BENEFIT_ID()
    url = urljoin(hostname, f'api/config/benefit/{benefit_id}/duration/sets')
    d = DATA_BENEFIT_DURATION(benefit_id)
    res = requests.post(url, json=d, **kwargs)
    data = res.json()
    if not res.ok: 
        raise Exception(res.text)

    for item in data:
        config_benefit_duration_set_id = item['config_benefit_duration_set_id']
        url = urljoin(hostname, f'api/config/benefit/{benefit_id}/duration/set/{config_benefit_duration_set_id}')
        default_item = item.get('duration_items')[-1]
        default_id = default_item.get('config_benefit_duration_detail_id')
        res = requests.patch(url, json={'default_config_benefit_duration_detail_id': default_id}, **kwargs)
        if not res.ok: 
            raise Exception(res.text)