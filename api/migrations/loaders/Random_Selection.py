import requests
import numpy as np
from requests.compat import urljoin
from app.auth import get_user
from app.extensions import db

from app.backend.models import (
    Model_ConfigBenefitVariationState,
    Model_ConfigProduct,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProvision,
    Model_ConfigProvisionState,
    Model_ConfigRatingMapperSet,
    Model_RefPlanStatus,
    Model_SelectionBenefit,
    Model_SelectionPlan,
)
from app.backend.schemas import Schema_ConfigBenefitVariationState_QuotableBenefits


def get_product(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def get_random_product_variation_state(product_id: int):
    PVS = Model_ConfigProductVariationState
    PV = Model_ConfigProductVariation
    product_variation_states = (
        db.session.query(PVS)
        .join(PV, PVS.config_product_variation_id == PV.config_product_variation_id)
        .filter(PV.config_product_id == product_id)
        .all()
    )
    random_row = np.random.randint(0, len(product_variation_states))
    return product_variation_states[random_row]


def get_random_benefits(plan: Model_SelectionPlan):
    benefits = Model_ConfigBenefitVariationState.find_quotable_benefits(
        plan.config_product_variation_state_id,
        plan.situs_state_id,
        plan.selection_plan_effective_date,
    )
    n_benefits = np.minimum(np.random.poisson(len(benefits) * 0.8), len(benefits))
    random_rows = np.random.choice(len(benefits), size=n_benefits, replace=False)
    return [b for i, b in enumerate(benefits) if i in random_rows]


def get_random_benefit_amount(benefit: dict):
    min_value = benefit.get("min_value")
    max_value = benefit.get("max_value")
    step_value = benefit.get("step_value")
    spread = (max_value - min_value) // step_value

    return min_value + step_value * np.random.randint(0, spread)


def get_random_benefit_duration(duration_set):
    if len(duration_set.duration_items) == 0:
        return None
    random_row = np.random.randint(0, len(duration_set.duration_items))
    return duration_set.duration_items[random_row]


def PROVISIONS(plan: Model_SelectionPlan):
    provision_states = Model_ConfigProvisionState.get_provision_states_by_product(
        plan.config_product_id, plan.situs_state_id
    )
    selections = []
    for provision_state in provision_states:
        provision = provision_state.provision
        data_type = provision.data_type.ref_attr_code
        dropdown_details = getattr(provision.dropdown_set, "dropdown_details", [])
        dropdown_items = [item.config_dropdown_detail_code for item in dropdown_details]

        if data_type == "string" and dropdown_items:
            value = np.random.choice(dropdown_items)
        if data_type == "string" and not dropdown_items:
            raise Exception(
                "Provisions with string data type must be selected from a valid dropdown list"
            )
        elif data_type == "boolean":
            value = np.random.choice([True, False])
        else:
            value = np.random.randint(100, 10000)
        selections.append(
            {
                "selection_plan_id": plan.selection_plan_id,
                "config_provision_state_id": provision_state.config_provision_state_id,
                "selection_value": str(value),
            }
        )
    return selections


def RATING_MAPPER_SETS(plan: Model_SelectionPlan):
    config_product = plan.config_product
    selection_rating_mapper_sets = []
    for i in range(1, 7):
        rating_mapper_collection_id = getattr(
            config_product, f"rating_mapper_collection_id{i}", None
        )
        if rating_mapper_collection_id is None:
            continue

        mapper_sets = Model_ConfigRatingMapperSet.find_all_by_attr(
            {
                "config_rating_mapper_collection_id": rating_mapper_collection_id,
            }
        )
        random_mapper_set = mapper_sets[np.random.randint(0, len(mapper_sets))]
        selection_rating_mapper_sets.append(
            {
                "selection_plan_id": plan.selection_plan_id,
                "config_rating_mapper_set_id": random_mapper_set.config_rating_mapper_set_id,
                "selection_rating_mapper_set_type": f"selection_rating_mapper_set_id{i}",
                "has_custom_weights": False,
                "mapper_details": [
                    {
                        "config_rating_mapper_detail_id": d.config_rating_mapper_detail_id,
                        "rate_table_attribute_detail_id": d.rate_table_attribute_detail_id,
                        "output_attribute_detail_id": d.output_attribute_detail_id,
                        "default_weight": float(d.weight),
                        "weight": float(d.weight),
                    }
                    for d in random_mapper_set.mapper_details
                ],
            }
        )
    return selection_rating_mapper_sets


def PLAN(product_code, owner):
    product = get_product(product_code)
    product_variation_state = get_random_product_variation_state(
        product.config_product_id
    )
    return {
        "config_product_id": product.config_product_id,
        "selection_plan_effective_date": str(
            product_variation_state.config_product_variation_state_effective_date
        ),
        "situs_state_id": product_variation_state.state_id,
        "config_product_variation_state_id": product_variation_state.config_product_variation_state_id,
        "cloned_from_selection_plan_id": None,
        "plan_status": Model_RefPlanStatus.find_one_by_attr(
            {"ref_attr_code": "in_progress"}
        ),
        "acl": [
            {
                "user_name": "superuser",
                "with_grant_option": True,
            },
            {
                "user_name": owner,
                "with_grant_option": True,
            },
        ],
    }


def BENEFITS(plan: Model_SelectionPlan):
    benefits = get_random_benefits(plan)
    schema = Schema_ConfigBenefitVariationState_QuotableBenefits(many=True)
    data = schema.dump(benefits)

    return [
        {
            "selection_plan_id": plan.selection_plan_id,
            "config_benefit_variation_state_id": d.get(
                "config_benefit_variation_state_id"
            ),
            "selection_value": get_random_benefit_amount(d),
        }
        for d in data
    ]


def BENEFIT_DURATION(benefit: Model_SelectionBenefit):
    duration_sets = benefit.config_benefit_variation_state.parent.durations
    items = []
    for duration_set in duration_sets:
        duration_item = get_random_benefit_duration(duration_set)
        if duration_item is None:
            continue
        items.append(
            {
                "selection_benefit_id": benefit.selection_benefit_id,
                "config_benefit_duration_set_id": duration_set.config_benefit_duration_set_id,
                "config_benefit_duration_detail_id": duration_item.config_benefit_duration_detail_id,
                "selection_factor": float(duration_item.config_benefit_duration_factor),
            }
        )
    return items


def AGE_BANDS(plan: Model_SelectionPlan):
    config_product_variation_state = plan.config_product_variation_state
    if config_product_variation_state.default_config_age_band_set_id is None:
        return [
            {
                "selection_plan_id": plan.selection_plan_id,
                "age_band_lower": 0,
                "age_band_upper": 999,
            }
        ]

    config_age_bands = config_product_variation_state.age_band_set.age_bands
    return [
        {
            "selection_plan_id": plan.selection_plan_id,
            "age_band_lower": ab.age_band_lower,
            "age_band_upper": ab.age_band_upper,
        }
        for ab in config_age_bands
    ]


def load(hostname: str, product_code: str, *args, **kwargs) -> None:
    user = get_user()

    # create plan
    url = urljoin(hostname, "api/selection/plan")
    data = PLAN(product_code, user["user_name"])
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    plan_data = res.json()
    plan = Model_SelectionPlan.find_one(plan_data["selection_plan_id"])

    # create mapper sets
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/mapper-sets")
    data = RATING_MAPPER_SETS(plan)
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    mapper_sets = res.json()

    # create age bands
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/age-bands")
    data = AGE_BANDS(plan)
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    age_bands = res.json()

    # create benefits
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/benefits")
    data = BENEFITS(plan)
    res = requests.post(url, json=data, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    benefit_data = res.json()
    benefits = Model_SelectionBenefit.find_by_plan(plan.selection_plan_id)

    for benefit in benefits:
        url = urljoin(
            hostname,
            f"api/selection/benefit/{benefit.selection_benefit_id}/durations",
        )
        duration_data = BENEFIT_DURATION(benefit)
        if not duration_data:
            continue

        res = requests.post(url, json=duration_data, **kwargs)
        if not res.ok:
            raise Exception(res.text)

    # create provisions
    provisions_data = PROVISIONS(plan)
    for prov in provisions_data:
        url = urljoin(
            hostname, f"api/selection/plan/{plan.selection_plan_id}/provision"
        )
        res = requests.post(url, json=prov, **kwargs)
        if not res.ok:
            raise Exception(res.text)

    return plan.selection_plan_id
