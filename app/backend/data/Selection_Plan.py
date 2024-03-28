import datetime
import requests
from requests.compat import urljoin

from ..models import (
    Model_ConfigProduct,
    Model_ConfigProductVariationState,
    Model_RefPlanStatus,
)


def get_product(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def DATA():
    product = get_product("CI21000")
    product_state = product.states[-1]
    state = product_state.state
    effective_date = product_state.config_product_state_effective_date
    product_variation_state = (
        Model_ConfigProductVariationState.find_one_for_selection_plan(
            product.config_product_id,
            "issue_age",
            state.state_code,
            effective_date,
        )
    )
    return {
        "config_product_id": product.config_product_id,
        "selection_plan_effective_date": str(effective_date),
        "situs_state_id": state.state_id,
        "config_product_variation_state_id": product_variation_state.config_product_variation_state_id,
        "cloned_from_selection_plan_id": None,
        "selection_group_id": None,
        "plan_status": Model_RefPlanStatus.find_one_by_attr(
            {"ref_attr_code": "in_progress"}
        ),
        "acl": [
            {
                "user_name": "superuser",
                "with_grant_option": True,
            },
            {
                "user_name": "cmsommerville",
                "with_grant_option": False,
            },
            {
                "role_name": "uw1000",
                "with_grant_option": False,
            },
        ],
    }


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/selection/plan")
    data = DATA()
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
