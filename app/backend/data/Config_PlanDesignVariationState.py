import numpy as np
import requests
from itertools import product
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigPlanDesignSet_Product,
)


def PRODUCT_VARIATION(product_code: str, variation_code: str):
    prd = Model_ConfigProduct.find_one_by_attr({"config_product_code": product_code})
    return Model_ConfigProductVariation.find_one_by_attr(
        {
            "config_product_id": prd.config_product_id,
            "config_product_variation_code": variation_code,
        }
    )


def PRODUCT_VARIATION_STATES(variation: Model_ConfigProductVariation):
    return Model_ConfigProductVariationState.find_all_by_attr(
        {"config_product_variation_id": variation.config_product_variation_id}
    )


def PRODUCT_PLAN_DESIGNS(product_id: int):
    return Model_ConfigPlanDesignSet_Product.find_by_parent(product_id)


def DATA(variation: Model_ConfigProductVariation):
    variation_states = PRODUCT_VARIATION_STATES(variation)
    plan_designs = PRODUCT_PLAN_DESIGNS(variation.config_product_id)
    return {
        "config_product_variation_state_id": [
            vs.config_product_variation_state_id
            for vs in variation_states
            if vs.config_product_variation_state_id % 5 != 0
        ],
        "config_plan_design_set_id": [
            pd.config_plan_design_set_id for pd in plan_designs
        ],
    }


def load(hostname: str, *args, **kwargs) -> None:
    VARIATION_CODES = ["issue_age", "attained_age"]
    for code in VARIATION_CODES:
        variation = PRODUCT_VARIATION("CI21000", code)
        vspd = DATA(variation)
        url = urljoin(
            hostname,
            f"api/config/variation/{variation.config_product_variation_id}/plan-designs:states",
        )
        res = requests.post(url, json=vspd, **kwargs)
        if not res.ok:
            raise Exception(res.text)

        variation_states = PRODUCT_VARIATION_STATES(variation)

        for vs in variation_states:
            if (
                vs.config_product_variation_state_id
                not in vspd["config_product_variation_state_id"]
            ):
                continue

            url = urljoin(
                hostname,
                f"api/config/variation/{variation.config_product_variation_id}/state/{vs.config_product_variation_state_id}",
            )
            val = int(np.random.choice(vspd["config_plan_design_set_id"]))
            res = requests.patch(
                url,
                json={"default_plan_design_set_id": val, "version_id": vs.version_id},
                **kwargs,
            )
            if not res.ok:
                raise Exception(res.text)
