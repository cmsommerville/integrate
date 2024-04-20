import requests
from requests.compat import urljoin

from app.models import (
    Model_ConfigProvision,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def DATA_GROUP_SIZE(plan: Model_SelectionPlan):
    provision = Model_ConfigProvision.find_one_by_attr(
        {"config_provision_code": "group_size"}
    )
    value = "3100"

    return {
        "selection_plan_id": plan.selection_plan_id,
        "config_provision_id": provision.config_provision_id,
        "selection_value": value,
    }


def DATA_SIC_CODE(plan: Model_SelectionPlan):
    provision = Model_ConfigProvision.find_one_by_attr(
        {"config_provision_code": "sic_code"}
    )
    value = "8182"

    return {
        "selection_plan_id": plan.selection_plan_id,
        "config_provision_id": provision.config_provision_id,
        "selection_value": value,
    }


def DATA_RED70(plan: Model_SelectionPlan):
    provision = Model_ConfigProvision.find_one_by_attr(
        {"config_provision_code": "reduction_at_70"}
    )
    value = "True"

    return {
        "selection_plan_id": plan.selection_plan_id,
        "config_provision_id": provision.config_provision_id,
        "selection_value": value,
    }


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/provision")
    res = requests.post(url, json=DATA_GROUP_SIZE(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)

    res = requests.post(url, json=DATA_SIC_CODE(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)

    res = requests.post(url, json=DATA_RED70(plan), **kwargs)
    if not res.ok:
        raise Exception(res.text)
