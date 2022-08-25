import requests
from requests.compat import urljoin

from  ..models import Model_ConfigProvision, Model_SelectionPlan

def PLAN(): 
    return Model_SelectionPlan.find_one_by_attr({
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
    })


def PROVISION(plan_id, provision_version_code):
    return Model_ConfigProvision.find_one_by_attr({
        'config_product_id': plan_id, 
        'config_provision_version_code': provision_version_code
    })

def DATA_SELECTION_PROVISIONS():
    plan_id = PLAN().selection_plan_id
    return [
        {
            'selection_plan_id': plan_id, 
            'config_provision_id': PROVISION(plan_id, 'std_group_size').config_provision_id, 
            'selection_provision_value': '1500',  
        }, 
        {
            'selection_plan_id': plan_id, 
            'config_provision_id': PROVISION(plan_id, 'std_sic_code').config_provision_id, 
            'selection_provision_value': '8082',  
        }, 
    ]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/selection/provision-list')
    res = requests.post(url, json=DATA_SELECTION_PROVISIONS())
    if not res.ok: 
        raise Exception(res.text)