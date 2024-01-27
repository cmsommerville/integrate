import requests
from requests.compat import urljoin

from ..models import (
    Model_RefCensusStrategy,
)


def DATA_PRODUCT():
    return [
        {
            "config_product_code": "CI21000",
            "config_product_label": "Critical Illness Series 21000",
            "config_product_effective_date": "2020-12-01",
            "config_product_expiration_date": "9999-12-31",
            "product_issue_date": "2021-01-01",
            "master_product_code": "CI",
            "form_code": "21000",
            "min_issue_age": 17,
            "max_issue_age": 99,
            "allow_employer_paid": True,
            "voluntary_census_strategy_id": Model_RefCensusStrategy.find_one_by_attr(
                {"ref_attr_code": "optional"}
            ).ref_id,
            "employer_paid_census_strategy_id": Model_RefCensusStrategy.find_one_by_attr(
                {"ref_attr_code": "required"}
            ).ref_id,
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/products")
    res = requests.post(url, json=DATA_PRODUCT())
    if not res.ok:
        raise Exception(res.text)
