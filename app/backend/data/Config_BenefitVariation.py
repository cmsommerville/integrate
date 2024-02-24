import requests
from requests.compat import urljoin
from itertools import product
from ..models import (
    Model_ConfigProductVariation,
    Model_ConfigBenefit,
    Model_ConfigProduct,
)


def PRODUCT_ID(code: str):
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": code}
    ).config_product_id


def VARIATIONS(product_id: int):
    return Model_ConfigProductVariation.find_by_product(product_id)


def BENEFITS(product_id: int):
    return Model_ConfigBenefit.find_by_product(product_id)


def DATA_BENEFIT_VARIATIONS(product_id, benefit_id):
    data = []
    variations = VARIATIONS(product_id)
    for pv in variations:
        data.append(
            {
                "config_benefit_id": benefit_id,
                "config_product_variation_id": pv.config_product_variation_id,
            }
        )
    return data


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID("CI21000")
    benefits = BENEFITS(product_id)
    for bnft in benefits:
        url = urljoin(
            hostname,
            f"api/config/product/{product_id}/benefit/{bnft.config_benefit_id}/variations",
        )
        res = requests.post(
            url,
            json=DATA_BENEFIT_VARIATIONS(product_id, bnft.config_benefit_id),
            **kwargs,
        )
        if not res.ok:
            raise Exception(res.text)
