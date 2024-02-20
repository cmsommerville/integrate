import requests
from requests.compat import urljoin

from ..models import (
    Model_ConfigBenefit,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def get_benefits(product_id: int):
    return Model_ConfigBenefit.find_by_product(product_id)


def DATA(plan: Model_SelectionPlan):
    benefits = get_benefits(plan.config_product_id)
    return [
        {
            "selection_plan_id": plan.selection_plan_id,
            "config_benefit_id": benefit.config_benefit_id,
            "selection_value": float(benefit.default_value),
        }
        for benefit in benefits
    ]


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/benefits")
    res = requests.post(url, json=DATA(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)
