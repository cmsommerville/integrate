import requests
from requests.compat import urljoin

from app.backend.models.Config_AttributeSet import Model_ConfigAttributeSet_Relationship
from  ..models import Model_ConfigAttributeDistributionSet_SmokerStatus, \
    Model_ConfigAttributeSet_SmokerStatus, Model_RefRatingStrategy, \
    Model_ConfigAttributeSet_Gender, Model_ConfigAttributeDistributionSet_Gender, \
    Model_RefCensusStrategy, Model_ConfigAgeDistributionSet

def DATA_PRODUCT():
    return [
    {
        'config_product_code': 'CI21000', 
        'config_product_label': 'Critical Illness Series 21000', 
        'config_product_effective_date': '2020-12-01', 
        'config_product_expiration_date': '9999-12-31', 
        'product_issue_date': '2021-01-01', 
        'master_product_code': 'CI', 
        'form_code': '21000', 
        'min_issue_age': 17, 
        'max_issue_age': 99, 

        'smoker_status_distribution_set_id': Model_ConfigAttributeDistributionSet_SmokerStatus.find_one_by_attr({
            'config_attr_distribution_set_label': 'N/T 85/15'
        }).config_attr_distribution_set_id, 
        'smoker_status_rating_strategy_id': Model_RefRatingStrategy.find_one_by_attr({
            "ref_attr_code": "rating"
        }).ref_id,
        'smoker_status_attr_set_id':Model_ConfigAttributeSet_SmokerStatus.find_one_by_attr({
            "config_attr_set_label": "Standard N/T/U"
        }).config_attr_set_id, 

        'gender_distribution_set_id': Model_ConfigAttributeDistributionSet_Gender.find_one_by_attr({
            'config_attr_distribution_set_label': 'Male/Female 50/50'
        }).config_attr_distribution_set_id, 
        'gender_rating_strategy_id': Model_RefRatingStrategy.find_one_by_attr({
            "ref_attr_code": "uw"
        }).ref_id,
        'gender_attr_set_id': Model_ConfigAttributeSet_Gender.find_one_by_attr({
            "config_attr_set_label": "Standard M/F/X"
        }).config_attr_set_id, 

        "age_distribution_set_id": Model_ConfigAgeDistributionSet.find_one_by_attr({
            "config_age_distribution_set_label": "Normal(45,15) Age Distribution"
        }).config_age_distribution_set_id, 
        "age_rating_strategy_id": Model_RefRatingStrategy.find_one_by_attr({
            "ref_attr_code": "rating"
        }).ref_id,

        'relationship_attr_set_id': Model_ConfigAttributeSet_Relationship.find_one_by_attr({
            "config_attr_set_label": "Standard EE/SP/CH"
        }).config_attr_set_id, 

        "allow_employer_paid": True,  
        "voluntary_census_strategy_id": Model_RefCensusStrategy.find_one_by_attr({
            "ref_attr_code": "optional"
        }).ref_id, 
        "employer_paid_census_strategy_id": Model_RefCensusStrategy.find_one_by_attr({
            "ref_attr_code": "required"
        }).ref_id, 
    }, 
]



def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, 'api/config/products')
    res = requests.post(url, json=DATA_PRODUCT())
    if not res.ok: 
        raise Exception(res.text)