import requests
from requests.compat import urljoin

from app.backend.models import (
    Model_ConfigBenefitVariationState,
    Model_SelectionPlan,
)
from app.backend.schemas import Schema_ConfigBenefitVariationState_QuotableBenefits


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def get_benefit_variation_states(benefit_variation_id: int, state_id: int):
    return Model_ConfigBenefitVariationState.find_one_by_attr(
        {
            "config_benefit_variation_id": benefit_variation_id,
            "state_id": state_id,
        }
    )


def DATA(plan: Model_SelectionPlan):
    objs = Model_ConfigBenefitVariationState.find_quotable_benefits(
        plan.config_product_variation_state_id,
        plan.situs_state_id,
        plan.selection_plan_effective_date,
    )
    schema = Schema_ConfigBenefitVariationState_QuotableBenefits(many=True)
    data = schema.dump(objs)

    return {
        "data": [
            {
                "selection_plan_id": plan.selection_plan_id,
                "config_benefit_variation_state_id": d.get(
                    "config_benefit_variation_state_id"
                ),
                "selection_value": d.get("default_value"),
            }
            for d in data
        ]
    }


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/benefits")
    res = requests.post(url, json=DATA(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)
