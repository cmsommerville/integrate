import requests
from requests.compat import urljoin
from ..models import Model_ConfigProduct


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def DATA_COVERAGE(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "config_coverage_code": "base",
            "config_coverage_label": "Base Benefits",
            "config_coverage_description": "Base Benefits",
        },
        {
            "config_product_id": product_id,
            "config_coverage_code": "heart_rider",
            "config_coverage_label": "Heart Rider",
            "config_coverage_description": "Heart Rider",
        },
        {
            "config_product_id": product_id,
            "config_coverage_code": "prog_benefits",
            "config_coverage_label": "Progressive Disease Rider",
            "config_coverage_description": "Progressive Disease Rider",
        },
        {
            "config_product_id": product_id,
            "config_coverage_code": "opt_benefits",
            "config_coverage_label": "Optional Benefits",
            "config_coverage_description": "Optional Benefits",
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/coverages")
    res = requests.post(url, json=DATA_COVERAGE(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
