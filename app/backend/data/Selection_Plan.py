import requests
from requests.compat import urljoin

from  ..models import Model_ConfigProductState, Model_ConfigProductVariation, \
    Model_ConfigProductMapperSet_Gender, Model_ConfigProductMapperSet_SmokerStatus, \
    Model_RefProductVariation, Model_RefAttrMapperType, Model_ConfigProduct

def PRODUCT():
    return Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    })

def PRODUCT_STATE(): 
    product = PRODUCT()
    return Model_ConfigProductState.find_one_by_attr({
        "config_product_id": product.config_product_id
    })

def PRODUCT_VARIATION(): 
    return Model_ConfigProductVariation.find_one_by_attr({
        "config_product_id": PRODUCT_STATE().config_product_id,
        "ref_product_variation_id": Model_RefProductVariation.find_one_by_attr({
            "ref_attr_code": "issue_age"
        }).ref_id
    })

def DATA_SELECTION_PLAN():
    return [
    {
        'selection_plan_description': 'TEST__SM_DISTINCT__GENDER_COMPOSITE',
        'selection_plan_effective_date': str(PRODUCT_STATE().config_product_state_effective_date), 
        'config_product_id': PRODUCT_STATE().config_product_id, 
        'state_id': PRODUCT_STATE().state_id, 
        'config_product_variation_id': PRODUCT_VARIATION().config_product_variation_id, 
        'config_gender_product_mapper_set_id': Model_ConfigProductMapperSet_Gender.find_one_by_attr({
            'config_attr_mapper_type_id': Model_RefAttrMapperType.find_one_by_attr({
                'ref_attr_code': 'composite'
            }).ref_id
        }).config_product_mapper_set_id, 
        'config_smoker_status_product_mapper_set_id': Model_ConfigProductMapperSet_SmokerStatus.find_one_by_attr({
            'config_attr_mapper_type_id': Model_RefAttrMapperType.find_one_by_attr({
                'ref_attr_code': 'distinct'
            }).ref_id
        }).config_product_mapper_set_id, 
        'is_employer_paid': False,  
    },
]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/selection/plan-list')
    res = requests.post(url, json=DATA_SELECTION_PLAN())
    if not res.ok: 
        raise Exception(res.text)