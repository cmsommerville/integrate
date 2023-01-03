import requests
from requests.compat import urljoin

from  ..models import Model_SelectionPlan

def PLAN(): 
    return Model_SelectionPlan.find_one_by_attr({
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
    }, last=True)

def load(hostname: str, *args, **kwargs) -> None:
    plan = PLAN()
    url = urljoin(hostname, f'api/selection/rate-table/{plan.selection_plan_id}')
    res = requests.post(url)
    if not res.ok: 
        raise Exception(res.text)