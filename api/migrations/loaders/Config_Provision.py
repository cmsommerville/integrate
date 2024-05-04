import requests
from requests.compat import urljoin
from app.backend.models import (
    Model_ConfigProduct,
    Model_RefDataTypes,
    Model_ConfigDropdownSet,
)


def PRODUCT(product_code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": product_code})


def DATA(product: Model_ConfigProduct):
    return [
        {
            "config_product_id": product.config_product_id,
            "config_provision_code": "group_size",
            "config_provision_label": "Group Size",
            "config_provision_data_type_id": Model_RefDataTypes.find_one_by_attr(
                {"ref_attr_code": "number"}
            ).ref_id,
            "config_provision_description": "This is the standard provision for CI21000 Group Size.",
            "default_value": None,
            "is_default_related_attribute": False,
        },
        {
            "config_product_id": product.config_product_id,
            "config_provision_code": "sic_code",
            "config_provision_label": "SIC",
            "config_provision_data_type_id": Model_RefDataTypes.find_one_by_attr(
                {"ref_attr_code": "string"}
            ).ref_id,
            "config_dropdown_set_id": Model_ConfigDropdownSet.find_one_by_attr(
                {"config_dropdown_set_label": "SIC Codes"}
            ).config_dropdown_set_id,
            "config_provision_description": "This is the standard provision for CI21000 SIC code.",
            "default_value": None,
            "is_default_related_attribute": False,
        },
        {
            "config_product_id": product.config_product_id,
            "config_provision_code": "reduction_at_70",
            "config_provision_label": "50% Benefit Reduction @ Age 70",
            "config_provision_data_type_id": Model_RefDataTypes.find_one_by_attr(
                {"ref_attr_code": "boolean"}
            ).ref_id,
            "config_provision_description": "This is the standard provision for CI21000 Reduction at Age 70.",
            "default_value": str(False),
            "is_default_related_attribute": True,
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    url = urljoin(
        hostname, f"api/config/product/{product.config_product_id}/provisions"
    )
    res = requests.post(url, json=DATA(product), **kwargs)
    if not res.ok:
        raise Exception(res.text)
