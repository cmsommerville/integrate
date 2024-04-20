import requests
from requests.compat import urljoin
from app.models import Model_ConfigProduct, Model_RefStates


def PRODUCT_ID(code: str):
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": code}
    ).config_product_id


def DATA_PRODUCT_STATES(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "AK"}).state_id,
            "config_product_state_effective_date": "2020-12-01",
            "config_product_state_expiration_date": "9999-12-31",
        },
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "AL"}).state_id,
            "config_product_state_effective_date": "2023-01-01",
            "config_product_state_expiration_date": "9999-12-31",
        },
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "SC"}).state_id,
            "config_product_state_effective_date": "2020-12-01",
            "config_product_state_expiration_date": "9999-12-31",
        },
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "NC"}).state_id,
            "config_product_state_effective_date": "2020-12-01",
            "config_product_state_expiration_date": "2022-12-31",
        },
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "TX"}).state_id,
            "config_product_state_effective_date": "2020-12-01",
            "config_product_state_expiration_date": "9999-12-31",
        },
        {
            "config_product_id": product_id,
            "state_id": Model_RefStates.find_one_by_attr({"state_code": "GA"}).state_id,
            "config_product_state_effective_date": "2022-12-01",
            "config_product_state_expiration_date": "9999-12-31",
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID("CI21000")
    url = urljoin(hostname, f"api/config/product/{product_id}/states")
    res = requests.post(url, json=DATA_PRODUCT_STATES(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
