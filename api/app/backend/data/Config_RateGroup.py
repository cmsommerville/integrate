import requests
from requests.compat import urljoin
from ..models import Model_ConfigProduct


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def DATA_RATE_GROUP(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "config_rate_group_code": "APU",
            "config_rate_group_label": "Annual Rate per $1000",
            "unit_value": 1000,
            "apply_discretionary_factor": True,
        },
        {
            "config_product_id": product_id,
            "config_rate_group_code": "FLAT",
            "config_rate_group_label": "Flat Rate",
            "unit_value": 1,
            "apply_discretionary_factor": False,
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/rate-groups")
    res = requests.post(url, json=DATA_RATE_GROUP(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
