import requests
from requests.compat import urljoin

from ..models import (
    Model_SelectionBenefit,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def get_benefits(plan: Model_SelectionPlan):
    return Model_SelectionBenefit.find_all_by_attr(
        {"selection_plan_id": plan.selection_plan_id}
    )


def DATA(benefit: Model_SelectionBenefit):
    duration_sets = (
        benefit.config_benefit_variation_state.benefit_variation.benefit.durations
    )
    return [
        {
            "selection_benefit_id": benefit.selection_benefit_id,
            "config_benefit_duration_set_id": duration_set.config_benefit_duration_set_id,
            "config_benefit_duration_detail_id": duration_set.duration_items[
                -1
            ].config_benefit_duration_detail_id,
            "selection_factor": float(
                duration_set.duration_items[-1].config_benefit_duration_factor
            ),
        }
        for duration_set in duration_sets
    ]


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    benefits = get_benefits(plan)
    for benefit in benefits:
        url = urljoin(
            hostname,
            f"api/selection/plan/{plan.selection_plan_id}/benefit/{benefit.selection_benefit_id}/durations",
        )
        duration_data = DATA(benefit)
        if not duration_data:
            continue

        res = requests.post(url, json=duration_data, **kwargs)
        if not res.ok:
            raise Exception(res.text)
