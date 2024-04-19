import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigProductVariation,
    Model_ConfigProductState,
    Model_ConfigAgeBandSet,
)


def PRODUCT(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def PRODUCT_VARIATION(product_code: str, variation_code: str):
    product = Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": product_code}
    )
    return Model_ConfigProductVariation.find_one_by_attr(
        {
            "config_product_id": product.config_product_id,
            "config_product_variation_code": variation_code,
        }
    )


def PRODUCT_STATES(product_code: str):
    product = Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": product_code}
    )
    return Model_ConfigProductState.find_all_by_attr(
        {"config_product_id": product.config_product_id}
    )


def DATA(variation: Model_ConfigProductVariation, product_code: str):
    return [
        {
            "config_product_variation_id": variation.config_product_variation_id,
            "state_id": product_state.state_id,
            "config_product_variation_state_effective_date": str(
                product_state.config_product_state_effective_date
            ),
            "config_product_variation_state_expiration_date": str(
                product_state.config_product_state_expiration_date
            ),
            "default_config_age_band_set_id": Model_ConfigAgeBandSet.find_one_by_attr(
                {"config_age_band_set_label": "Standard 10 Year Age Bands"}
            ).config_age_band_set_id,
        }
        for product_state in PRODUCT_STATES(product_code)
    ]


def load(hostname: str, *args, **kwargs) -> None:
    PRODUCT_CODE = "CI21000"
    product = PRODUCT(PRODUCT_CODE)

    variation = PRODUCT_VARIATION(PRODUCT_CODE, "issue_age")
    data = DATA(variation, PRODUCT_CODE)
    url = urljoin(
        hostname,
        f"api/config/variation/{variation.config_product_variation_id}/states",
    )
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)

    variation = PRODUCT_VARIATION(PRODUCT_CODE, "attained_age")
    data = DATA(variation, PRODUCT_CODE)
    url = urljoin(
        hostname,
        f"api/config/variation/{variation.config_product_variation_id}/states",
    )
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
