import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigBenefit,
    Model_ConfigBenefitVariation,
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


def BENEFIT_VARIATION(benefit_code: str):
    benefit = Model_ConfigBenefit.find_one_by_attr(
        {"config_benefit_code": benefit_code}
    )
    return Model_ConfigBenefitVariation.find_by_benefit(benefit.config_benefit_id)


def DATA(product: Model_ConfigProduct, benefit_variation: Model_ConfigBenefitVariation):
    return [
        {
            "config_benefit_variation_id": benefit_variation.config_benefit_variation_id,
            "state_id": state.state_id,
            "config_benefit_variation_state_effective_date": str(
                product.config_product_effective_date
            ),
            "config_benefit_variation_state_expiration_date": str(
                product.config_product_expiration_date
            ),
            "config_rate_table_set_id": None,
        }
        for state in product.states
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    for bnft_code in BENEFITS:
        benefit_variations = BENEFIT_VARIATION(bnft_code)

        for variation in benefit_variations:
            data = DATA(product, variation)
            url = urljoin(
                hostname,
                f"api/config/product/{product.config_product_id}/benefit-variation/{variation.config_benefit_variation_id}/states",
            )
            res = requests.post(url, json=data, **kwargs)
            if not res.ok:
                raise Exception(res.text)
