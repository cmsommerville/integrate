import requests
from requests.compat import urljoin

from  ..models import Model_SelectionPlan

def PLAN(): 
    return Model_SelectionPlan.find_one_by_attr({
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
    })


def DATA_SELECTION_AGE_BANDS():
    plan_id = PLAN().selection_plan_id
    return [
        {
            'selection_plan_id': plan_id, 
            'lower_age_value': 18, 
            'upper_age_value': 29,
        }, 
        {
            'selection_plan_id': plan_id, 
            'lower_age_value': 30, 
            'upper_age_value': 39,
        }, 
        {
            'selection_plan_id': plan_id, 
            'lower_age_value': 40, 
            'upper_age_value': 49,
        }, 
        {
            'selection_plan_id': plan_id, 
            'lower_age_value': 50, 
            'upper_age_value': 59,
        }, 
        {
            'selection_plan_id': plan_id, 
            'lower_age_value': 60, 
            'upper_age_value': 99,
        }, 
    ]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/selection/age-band-list')
    res = requests.post(url, json=DATA_SELECTION_AGE_BANDS())
    if not res.ok: 
        raise Exception(res.text)