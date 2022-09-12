import requests
from requests.compat import urljoin

from  ..models import Model_ConfigBenefitProductVariation, Model_SelectionPlan

def PLAN(): 
    return Model_SelectionPlan.find_one_by_attr({
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
    }, last=True)


def BENEFITS(product_variation_id):
    return Model_ConfigBenefitProductVariation.find_all_by_attr({
        'config_product_variation_id': product_variation_id
    })

def DATA_SELECTION_BENEFITS():
    return [
        {
            'selection_plan_id': PLAN().selection_plan_id, 
            'config_benefit_product_variation_id': bnft.config_benefit_product_variation_id, 
            'config_benefit_id': bnft.config_benefit_id, 
            'selection_benefit_value': float(bnft.benefit.default_value),  
        }
        for bnft in BENEFITS(PLAN().config_product_variation_id)
    ]


def load(hostname: str) -> None:
    url = urljoin(hostname, 'api/crud/selection/benefit-list')
    res = requests.post(url, json=DATA_SELECTION_BENEFITS())
    if not res.ok: 
        raise Exception(res.text)