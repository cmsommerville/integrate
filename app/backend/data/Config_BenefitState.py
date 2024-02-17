import requests
from requests.compat import urljoin
from ..models import Model_ConfigProduct, Model_ConfigBenefit

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


def BENEFIT(product: Model_ConfigProduct, benefit_code: str):
    return Model_ConfigBenefit.find_one_by_attr(
        {
            "config_benefit_code": benefit_code,
            "config_product_id": product.config_product_id,
        }
    )


def DATA(product: Model_ConfigProduct, benefit: Model_ConfigBenefit):
    return [
        {
            "config_benefit_id": benefit.config_benefit_id,
            "state_id": state.state_id,
            "config_benefit_state_effective_date": str(
                product.config_product_effective_date
            ),
            "config_benefit_state_expiration_date": str(
                product.config_product_expiration_date
            ),
        }
        for state in product.states
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    for bnft_code in BENEFITS:
        benefit = BENEFIT(product, bnft_code)
        url = urljoin(
            hostname,
            f"api/config/product/{product.config_product_id}/benefit/{benefit.config_benefit_id}/states",
        )
        res = requests.post(url, json=DATA(product, benefit), **kwargs)
        if not res.ok:
            raise Exception(res.text)
