import requests
from requests.compat import urljoin
from app.backend.models import Model_ConfigProduct


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def DATA_PRODUCT_VARIATION(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "config_product_variation_code": "issue_age",
            "config_product_variation_label": "Issue Age",
        },
        {
            "config_product_id": product_id,
            "config_product_variation_code": "attained_age",
            "config_product_variation_label": "Attained Age",
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/variations")
    res = requests.post(url, json=DATA_PRODUCT_VARIATION(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
