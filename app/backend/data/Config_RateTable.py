import numpy as np
import requests
from requests.compat import urljoin
from itertools import product
from ..models import Model_ConfigProduct, Model_ConfigBenefitVariation


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


# def GENDERS(composite: bool):
#     data = Model_ConfigAttributeSet_Gender.find_one_by_attr({
#         'config_attr_set_label': 'Standard M/F/X'
#     }).attributes
#     return [x for x in data if x.is_composite_id == composite]

# def SMOKER_STATUSES(composite: bool):
#     data = Model_ConfigAttributeSet_SmokerStatus.find_one_by_attr({
#         'config_attr_set_label': 'Standard N/T/U'
#     }).attributes
#     return [x for x in data if x.is_composite_id == composite]

# def RELATIONSHIPS():
#     return Model_ConfigAttributeSet_Relationship.find_one_by_attr({
#         'config_attr_set_label': 'Standard EE/SP/CH'
#     }).attributes


def BENEFIT_VARIATIONS():
    return Model_ConfigBenefitVariation.find_all()


def DATA_RATE_TABLE():
    data = []
    betas = [1, 0.1, 0.005, 0.5, 0.5, 0.5]

    for bpv, age, gndr, smkr, rel in product(
        BENEFIT_VARIATIONS(), range(22, 72, 5)
    ):  # , GENDERS(True), SMOKER_STATUSES(False), RELATIONSHIPS(), ):
        xs = [
            bpv.config_benefit_product_variation_id % 5,
            age,
            age**2,
            (gndr.config_attr_detail_id % 2),
            (smkr.config_attr_detail_id % 2),
            (rel.config_attr_detail_id % 2),
        ]
        data.append(
            {
                "config_benefit_product_variation_id": bpv.config_benefit_product_variation_id,
                "age_value": age,
                "config_gender_detail_id": gndr.config_attr_detail_id,
                "config_smoker_status_detail_id": smkr.config_attr_detail_id,
                "config_relationship_detail_id": rel.config_attr_detail_id,
                "annual_rate_per_unit": np.random.normal(np.dot(betas, xs), scale=0.3),
                "unit_value": 1000,
            }
        )
    return data


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/rate-tables")
    res = requests.post(url, json=DATA_RATE_TABLE(), **kwargs)
    if not res.ok:
        raise Exception(res.text)
