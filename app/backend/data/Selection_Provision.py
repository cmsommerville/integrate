import requests
from requests.compat import urljoin

from ..models import (
    Model_ConfigProvision,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def get_provisions(product_id: int):
    return Model_ConfigProvision.find_by_product(product_id)


def DATA(plan: Model_SelectionPlan):
    provisions = get_provisions(plan.config_product_id)
    return [
        {
            "selection_plan_id": plan.selection_plan_id,
            "config_provision_id": provision.config_provision_id,
            "config_provision_type_code": provision.config_provision_type_code,
            "selection_value": 1,
        }
        for provision in provisions
    ]


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/benefits")
    res = requests.post(url, json=DATA(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)
