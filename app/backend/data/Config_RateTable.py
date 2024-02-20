import numpy as np
import pandas as pd
import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigBenefit,
    Model_RefRateFrequency,
)
from ..classes.RateTableCohorts import RateTableCohorts


def PRODUCT(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def BENEFITS(product_id: int):
    return Model_ConfigBenefit.find_by_product(product_id)


def RATESET(product: Model_ConfigProduct, benefit: Model_ConfigBenefit):
    rate_table_cohorts = RateTableCohorts(product.config_product_id)
    cohorts = rate_table_cohorts.cohorts_for_rate_table()
    rate_frequency_id = Model_RefRateFrequency.find_one_by_attr(
        {"ref_attr_code": "1pp"}
    ).ref_id

    rating_mapper_collections = {
        f"rating_mapper_collection_id{k}": v
        for k, v in rate_table_cohorts.rating_mapper_collections.items()
    }

    return {
        **rating_mapper_collections,
        "age_distribution_set_id": rate_table_cohorts.age_distribution_set_id,
        "config_rate_table_set_label": "Standard Rates",
        "config_benefit_id": benefit.config_benefit_id,
        "rates": [
            {
                **row,
                "rate_per_unit": row["rating_age"] * 0.1,
                "rate_frequency_id": rate_frequency_id,
                "rate_unit_value": 1,
            }
            for row in cohorts
        ],
    }


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    benefits = BENEFITS(product.config_product_id)

    for benefit in benefits:
        rateset = RATESET(product, benefit)

        url = urljoin(
            hostname,
            f"api/config/product/{product.config_product_id}/benefit/{benefit.config_benefit_id}/rateset",
        )
        res = requests.post(url, json=rateset, **kwargs)
        if not res.ok:
            raise Exception(res.text)
