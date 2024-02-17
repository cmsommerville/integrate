import requests
from requests.compat import urljoin

from ..models import (
    Model_ConfigAgeDistributionSet,
    Model_ConfigRatingMapperCollection,
    Model_RefRatingStrategy,
    Model_RefCensusStrategy,
)


def get_rating_strategy(strategy: str):
    return Model_RefRatingStrategy.find_one_by_attr({"ref_attr_code": strategy}).ref_id


def get_age_distribution_set(label: str):
    return Model_ConfigAgeDistributionSet.find_one_by_attr(
        {"config_age_distribution_set_label": label}
    ).config_age_distribution_set_id


def get_rating_mapper_collection(label: str):
    return Model_ConfigRatingMapperCollection.find_one_by_attr(
        {"config_rating_mapper_collection_label": label}
    ).config_rating_mapper_collection_id


def get_census_strategy(code: str):
    return Model_RefCensusStrategy.find_one_by_attr({"ref_attr_code": code}).ref_id


def DATA():
    return [
        {
            "config_product_code": "CI21000",
            "config_product_label": "Critical Illness Series 21000",
            "config_product_effective_date": "2020-12-01",
            "config_product_expiration_date": "9999-12-31",
            "product_issue_date": "2021-01-01",
            "master_product_code": "CI",
            "form_code": "21000",
            "age_rating_strategy_id": get_rating_strategy("rating"),
            "age_distribution_set_id": get_age_distribution_set(
                "Normal(45,15) Age Distribution"
            ),
            "rating_mapper_collection_id1": get_rating_mapper_collection(
                "Standard Smoker Status Mappers"
            ),
            "rating_mapper_collection_id2": get_rating_mapper_collection(
                "Standard Gender Mappers"
            ),
            "rating_mapper_collection_id3": get_rating_mapper_collection(
                "Standard Relationship Mappers"
            ),
            "allow_employer_paid": True,
            "voluntary_census_strategy_id": get_census_strategy("required"),
            "employer_paid_census_strategy_id": get_census_strategy("required"),
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/products")
    res = requests.post(url, json=DATA(), **kwargs)
    if not res.ok:
        raise Exception(res.text)
