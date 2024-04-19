import requests
from requests.compat import urljoin

from ..models import (
    Model_SelectionAgeBand,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def DATA(plan: Model_SelectionPlan, lower_ages=[0, 30, 40, 50, 60]):
    return [
        {
            "selection_plan_id": plan.selection_plan_id,
            "age_band_lower": lower,
            "age_band_upper": lower_ages[i + 1] - 1 if i + 1 < len(lower_ages) else 999,
        }
        for i, lower in enumerate(lower_ages)
    ]


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/age-bands")
    res = requests.post(url, json=DATA(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)
