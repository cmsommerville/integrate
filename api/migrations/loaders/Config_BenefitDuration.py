import requests
import json
from requests.compat import urljoin
from app.backend.models import Model_ConfigBenefit, Model_ConfigProduct


def PRODUCT(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def BENEFIT(product: Model_ConfigProduct, benefit_code: str):
    return Model_ConfigBenefit.find_one_by_attr(
        {
            "config_benefit_code": benefit_code,
            "config_product_id": product.config_product_id,
        }
    )


def DATA_BENEFIT_DURATION(benefit_id: int):
    return [
        {
            "config_benefit_id": benefit_id,
            "config_benefit_duration_set_code": "annual_payments",
            "config_benefit_duration_set_label": "Number of Payments per Year",
            "duration_items": [
                {
                    "config_benefit_duration_detail_code": "1",
                    "config_benefit_duration_detail_label": "1 per year",
                    "config_benefit_duration_factor": 0.85,
                    "is_restricted": False,
                },
                {
                    "config_benefit_duration_detail_code": "2",
                    "config_benefit_duration_detail_label": "2 per year",
                    "config_benefit_duration_factor": 0.95,
                    "is_restricted": False,
                },
                {
                    "config_benefit_duration_detail_code": "3",
                    "config_benefit_duration_detail_label": "3 per year",
                    "config_benefit_duration_factor": 1,
                    "is_restricted": False,
                },
                {
                    "config_benefit_duration_detail_code": "4",
                    "config_benefit_duration_detail_label": "4 per year",
                    "config_benefit_duration_factor": 1.1,
                    "is_restricted": True,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    benefit = BENEFIT(product, "skin_cancer")
    url = urljoin(
        hostname,
        f"api/config/benefit/{benefit.config_benefit_id}/durations",
    )
    d = DATA_BENEFIT_DURATION(benefit.config_benefit_id)
    res = requests.post(url, json=d, **kwargs)
    data = res.json()
    if not res.ok:
        raise Exception(res.text)

    # set default duration detail item to last one
    for item in data["data"]:
        config_benefit_duration_set_id = item["config_benefit_duration_set_id"]
        version_id = item["version_id"]
        url = urljoin(
            hostname,
            f"api/config/benefit/{benefit.config_benefit_id}/duration/{config_benefit_duration_set_id}",
        )
        default_item = item.get("duration_items")[-1]
        default_id = default_item.get("config_benefit_duration_detail_id")
        res = requests.patch(
            url,
            json={
                "default_config_benefit_duration_detail_id": default_id,
                "version_id": version_id,
            },
            **kwargs,
        )
        if not res.ok:
            raise Exception(res.text)
