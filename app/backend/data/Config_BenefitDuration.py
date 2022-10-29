import requests
import json
from requests.compat import urljoin
from  ..models import Model_ConfigBenefit, Model_RefBenefit

def DATA_BENEFIT_DURATION():
    return [
    {
        'config_benefit_id': Model_ConfigBenefit.find_one_by_attr({
            "ref_benefit_id": Model_RefBenefit.find_one_by_attr({
                "ref_attr_code": "skin_cancer"
            }).ref_id
        }).config_benefit_id, 
        'config_benefit_duration_set_code': 'annual_payments', 
        'config_benefit_duration_set_label': "Number of Payments per Year", 
        "duration_items": [
            {
                "config_benefit_duration_detail_code": "1", 
                "config_benefit_duration_detail_label": "1 per year", 
                "config_benefit_duration_factor": 0.85, 
            }, 
            {
                "config_benefit_duration_detail_code": "2", 
                "config_benefit_duration_detail_label": "2 per year", 
                "config_benefit_duration_factor": 0.95, 
            }, 
            {
                "config_benefit_duration_detail_code": "3", 
                "config_benefit_duration_detail_label": "3 per year", 
                "config_benefit_duration_factor": 1, 
            }, 
            {
                "config_benefit_duration_detail_code": "4", 
                "config_benefit_duration_detail_label": "4 per year", 
                "config_benefit_duration_factor": 1.1, 
            }, 
        ]
    }, 
]



def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/config/benefit-duration-set-list')
    res = requests.post(url, json=DATA_BENEFIT_DURATION())
    data = res.json()
    if not res.ok: 
        raise Exception(res.text)

    for item in data:
        config_benefit_duration_set_id = item['config_benefit_duration_set_id']
        url = urljoin(hostname, f'api/crud/config/benefit-duration-set/{config_benefit_duration_set_id}')
        default_id = item.get('duration_items')[-1]
        res = requests.patch(url, json={'default_config_benefit_duration_detail_id': default_id})
        if not res.ok: 
            raise Exception(res.text)