import requests
from requests.compat import urljoin

from app.models import (
    Model_ConfigRatingMapperSet,
    Model_SelectionPlan,
)


def get_plan():
    PLAN = Model_SelectionPlan
    return PLAN.query.order_by(PLAN.selection_plan_id.desc()).first()


def get_rating_mapper_set(
    selection_plan_id: int, collection_id: int, label: str, type_code: str
):
    mapper_set = Model_ConfigRatingMapperSet.find_one_by_attr(
        {
            "config_rating_mapper_collection_id": collection_id,
            "config_rating_mapper_set_label": label,
        }
    )
    return {
        "selection_plan_id": selection_plan_id,
        "config_rating_mapper_set_id": mapper_set.config_rating_mapper_set_id,
        "selection_rating_mapper_set_type": type_code,
        "has_custom_weights": False,
        "mapper_details": [
            {
                "config_rating_mapper_detail_id": d.config_rating_mapper_detail_id,
                "rate_table_attribute_detail_id": d.rate_table_attribute_detail_id,
                "output_attribute_detail_id": d.output_attribute_detail_id,
                "default_weight": float(d.weight),
                "weight": float(d.weight),
            }
            for d in mapper_set.mapper_details
        ],
    }


def load(hostname: str, *args, **kwargs) -> None:
    plan = get_plan()

    set1 = get_rating_mapper_set(
        plan.selection_plan_id,
        plan.config_product.rating_mapper_collection_id1,
        "Tobacco Distinct",
        "selection_rating_mapper_set_id1",
    )
    set2 = get_rating_mapper_set(
        plan.selection_plan_id,
        plan.config_product.rating_mapper_collection_id2,
        "50/50 Male/Female Composite",
        "selection_rating_mapper_set_id2",
    )
    set3 = get_rating_mapper_set(
        plan.selection_plan_id,
        plan.config_product.rating_mapper_collection_id3,
        "Relationship Distinct",
        "selection_rating_mapper_set_id3",
    )
    DATA = [set1, set2, set3]
    url = urljoin(hostname, f"api/selection/plan/{plan.selection_plan_id}/mapper-sets")
    res = requests.post(url, json=DATA, **kwargs)
    if not res.ok:
        raise Exception(res.text)
