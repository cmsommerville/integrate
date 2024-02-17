import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_RefAttrMapperType,
    Model_ConfigAttributeDetail,
)


def _PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def _COMPOSITE():
    return Model_RefAttrMapperType.find_one_by_attr({"ref_attr_code": "composite"})


def _DISTINCT():
    return Model_RefAttrMapperType.find_one_by_attr({"ref_attr_code": "distinct"})


def DATA_PRODUCT_MAPPER__GENDER(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "config_attr_type_code": "gender",
            "config_attr_mapper_type_id": _COMPOSITE().ref_id,
            "is_default": True,
            "mappers": [
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "X"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "X"}
                    ).config_attr_detail_id,
                },
            ],
        },
        {
            "config_product_id": product_id,
            "config_attr_type_code": "gender",
            "config_attr_mapper_type_id": _DISTINCT().ref_id,
            "is_default": False,
            "mappers": [
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "M"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "M"}
                    ).config_attr_detail_id,
                },
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "F"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "F"}
                    ).config_attr_detail_id,
                },
            ],
        },
    ]


def DATA_PRODUCT_MAPPER__SMOKER_STATUS(product_id: int):
    return [
        {
            "config_product_id": product_id,
            "config_attr_type_code": "smoker_status",
            "config_attr_mapper_type_id": _COMPOSITE().ref_id,
            "is_default": False,
            "mappers": [
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "N"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "U"}
                    ).config_attr_detail_id,
                },
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "T"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "U"}
                    ).config_attr_detail_id,
                },
            ],
        },
        {
            "config_product_id": product_id,
            "config_attr_type_code": "smoker_status",
            "config_attr_mapper_type_id": _DISTINCT().ref_id,
            "is_default": True,
            "mappers": [
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "N"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "N"}
                    ).config_attr_detail_id,
                },
                {
                    "from_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "T"}
                    ).config_attr_detail_id,
                    "to_config_attr_detail_id": Model_ConfigAttributeDetail.find_one_by_attr(
                        {"config_attr_detail_code": "T"}
                    ).config_attr_detail_id,
                },
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = _PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/mapper/sets/gender")
    res = requests.post(url, json=DATA_PRODUCT_MAPPER__GENDER(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)

    url = urljoin(
        hostname, f"api/config/product/{product_id}/mapper/sets/smoker_status"
    )
    res = requests.post(
        url, json=DATA_PRODUCT_MAPPER__SMOKER_STATUS(product_id), **kwargs
    )
    if not res.ok:
        raise Exception(res.text)
