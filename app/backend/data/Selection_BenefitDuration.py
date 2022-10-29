import requests
from requests.compat import urljoin

from  ..models import Model_ConfigBenefitDurationSet, Model_ConfigBenefitDurationDetail, \
    Model_SelectionPlan, Model_SelectionBenefit

def PLAN(): 
    return Model_SelectionPlan.find_one_by_attr({
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
    }, last=True)

def BENEFITS(plan_id):
    return Model_SelectionBenefit.find_by_plan(plan_id)

def DATA_SELECTION_BENEFIT_DURATIONS():
    plan = PLAN()
    sel = []
    for bnft in BENEFITS(plan.selection_plan_id):
        config_benefit = getattr(bnft, 'config_benefit', None)
        if config_benefit is None:
            raise Exception("Cannot find config_benefit relationship on SelectionBenefitDuration")

        durations = getattr(config_benefit, 'durations', None)
        if durations is None:
            continue
        if len(durations) == 0: 
            continue

        sel.extend([{
                'selection_benefit_id': bnft.selection_benefit_id, 
                'config_benefit_duration_set_id': durset.duration_items[0].config_benefit_duration_set_id, 
                'config_benefit_duration_detail_id': durset.duration_items[0].config_benefit_duration_detail_id, 
                'selection_benefit_duration_factor': float(durset.duration_items[0].config_benefit_duration_factor), 
            } 
            for durset in durations])
    print(sel)
    return sel


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/crud/selection/benefit-duration-list')
    res = requests.post(url, json=DATA_SELECTION_BENEFIT_DURATIONS())
    if not res.ok: 
        raise Exception(res.text)