import requests
from typing import List
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
)

BENEFITS = [
    "cancer",
    "heart_attack",
    "stroke",
    "renal_failure",
    "transplant",
    "wellness",
    "skin_cancer",
]


def PRODUCT(product_code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": product_code})


def VARIATION(product: Model_ConfigProduct, variation_code: str):
    return Model_ConfigProductVariation.find_one_by_attr(
        {
            "config_product_id": product.config_product_id,
            "config_product_variation_code": variation_code,
        }
    )


def VARIATION_STATES(variation_id: int):
    return Model_ConfigProductVariationState.find_all_by_attr(
        {"config_product_variation_id": variation_id}
    )


def BENEFITS(product_id: int):
    return Model_ConfigBenefit.find_by_product(product_id)


def DATA(
    product: Model_ConfigProduct,
    benefit: Model_ConfigBenefit,
    variation_states: List[Model_ConfigProductVariationState],
):
    return [
        {
            "config_benefit_id": benefit.config_benefit_id,
            "config_product_variation_state_id": vs.config_product_variation_state_id,
            "state_id": vs.state_id,
            "config_benefit_variation_state_effective_date": str(
                product.config_product_effective_date
            ),
            "config_benefit_variation_state_expiration_date": str(
                product.config_product_expiration_date
            ),
            "config_rate_table_set_id": None,
        }
        for vs in variation_states
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    product_variation = VARIATION(product, "issue_age")
    variation_states = VARIATION_STATES(product_variation.config_product_variation_id)
    benefits = BENEFITS(product.config_product_id)
    for benefit in benefits:
        data = DATA(product, benefit, variation_states)
        url = urljoin(
            hostname,
            f"api/config/benefit/{benefit.config_benefit_id}/states",
        )
        res = requests.post(url, json=data, **kwargs)
        if not res.ok:
            raise Exception(res.text)
