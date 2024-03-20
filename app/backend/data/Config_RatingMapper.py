import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigAttributeSet,
    Model_ConfigAttributeDetail,
    Model_RefRatingStrategy,
)


def ATTR_SET_ID(config_attr_set_code: str):
    return Model_ConfigAttributeSet.find_one_by_attr(
        {"config_attr_set_code": config_attr_set_code}
    ).config_attr_set_id


def ATTR_DETAIL_ID(set_id: int, config_attr_detail_code: str):
    return Model_ConfigAttributeDetail.find_one_by_attr(
        {
            "config_attr_detail_code": config_attr_detail_code,
            "config_attr_set_id": set_id,
        }
    ).config_attr_detail_id


def RATING_STRATEGY(code: str):
    return Model_RefRatingStrategy.find_one_by_attr({"ref_attr_code": code})


def DATA():
    return [
        {
            "config_attribute_set_id": ATTR_SET_ID("gender"),
            "config_rating_mapper_collection_label": "Standard Gender Mappers",
            "rating_strategy_id": RATING_STRATEGY("uw").ref_id,
            "is_selectable": False,
            "can_override_distribution": True,
            "mapper_sets": [
                {
                    "config_rating_mapper_set_label": "50/50 Male/Female Composite",
                    "is_composite": True,
                    "is_employer_paid": False,
                    "mapper_details": [
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("gender"), "M"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("gender"), "X"
                            ),
                            "weight": 0.5,
                        },
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("gender"), "F"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("gender"), "X"
                            ),
                            "weight": 0.5,
                        },
                    ],
                },
            ],
        },
        {
            "config_attribute_set_id": ATTR_SET_ID("smoker_status"),
            "config_rating_mapper_collection_label": "Standard Smoker Status Mappers",
            "rating_strategy_id": RATING_STRATEGY("rating").ref_id,
            "is_selectable": True,
            "can_override_distribution": True,
            "mapper_sets": [
                {
                    "config_rating_mapper_set_label": "85/15 Non-Tobacco/Tobacco Composite",
                    "is_composite": True,
                    "is_employer_paid": False,
                    "mapper_details": [
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "T"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "U"
                            ),
                            "weight": 0.15,
                        },
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "N"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "U"
                            ),
                            "weight": 0.85,
                        },
                    ],
                },
                {
                    "config_rating_mapper_set_label": "Tobacco Distinct",
                    "is_composite": False,
                    "is_employer_paid": False,
                    "mapper_details": [
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "T"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "T"
                            ),
                            "weight": 1,
                        },
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "N"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("smoker_status"), "N"
                            ),
                            "weight": 1,
                        },
                    ],
                },
            ],
        },
        {
            "config_attribute_set_id": ATTR_SET_ID("relationship"),
            "config_rating_mapper_collection_label": "Standard Relationship Mappers",
            "rating_strategy_id": RATING_STRATEGY("rating").ref_id,
            "is_selectable": False,
            "can_override_distribution": False,
            "mapper_sets": [
                {
                    "config_rating_mapper_set_label": "Relationship Distinct",
                    "is_composite": False,
                    "is_employer_paid": False,
                    "mapper_details": [
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("relationship"), "EE"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("relationship"), "EE"
                            ),
                            "weight": 1,
                        },
                        {
                            "rate_table_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("relationship"), "SP"
                            ),
                            "output_attribute_detail_id": ATTR_DETAIL_ID(
                                ATTR_SET_ID("relationship"), "SP"
                            ),
                            "weight": 1,
                        },
                    ],
                },
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    url = urljoin(hostname, "api/config/mappers")
    res = requests.post(url, json=DATA(), **kwargs)
    if not res.ok:
        raise Exception(res.text)
