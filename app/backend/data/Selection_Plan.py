import requests
from requests.compat import urljoin

from ..models import (
    Model_ConfigProduct,
    Model_ConfigProductVariation,
    Model_ConfigRatingMapperCollection,
    Model_ConfigRatingMapperSet,
    Model_RefPlanStatus,
    Model_SelectionPlan,
)


def get_product(code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": code})


def get_product_variation(product_id: int, code: str):
    return Model_ConfigProductVariation.find_one_by_attr(
        {"config_product_id": product_id, "config_product_variation_code": code}
    )


def get_rating_mapper_set(collection_id: int, label: str):
    return Model_ConfigRatingMapperSet.find_one_by_attr(
        {
            "config_rating_mapper_collection_id": collection_id,
            "config_rating_mapper_set_label": label,
        }
    ).config_rating_mapper_set_id


def DATA():
    product = get_product("CI21000")
    product_variation = get_product_variation(product.config_product_id, "issue_age")
    return {
        "config_product_id": product.config_product_id,
        "selection_plan_effective_date": str(product.config_product_effective_date),
        "situs_state_id": product.states[-1].state_id,
        "config_product_variation_id": product_variation.config_product_variation_id,
        "cloned_from_selection_plan_id": None,
        "plan_status": Model_RefPlanStatus.find_one_by_attr(
            {"ref_attr_code": "in_progress"}
        ),
        "selection_rating_mapper_set_id1": get_rating_mapper_set(
            product.rating_mapper_collection_id1,
            "Tobacco Distinct",
        ),
        "selection_rating_mapper_set_id2": get_rating_mapper_set(
            product.rating_mapper_collection_id2,
            "50/50 Male/Female Composite",
        ),
        "selection_rating_mapper_set_id3": get_rating_mapper_set(
            product.rating_mapper_collection_id3,
            "Relationship Distinct",
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
    res = requests.post(url, json=DATA(), **kwargs)
    if not res.ok:
        raise Exception(res.text)
