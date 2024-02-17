import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProvision,
    Model_RefComparisonOperator,
    Model_RefDataTypes,
    Model_ConfigProduct,
)


def PRODUCT(product_code: str):
    return Model_ConfigProduct.find_one_by_attr({"config_product_code": product_code})


def PROVISION(product: Model_ConfigProduct, provision_code: str):
    return Model_ConfigProvision.find_one_by_attr(
        {
            "config_provision_code": provision_code,
            "config_product_id": product.config_product_id,
        }
    )


def DATA_GROUP_SIZE(provision: Model_ConfigProvision):
    return [
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 1,
            "factor_value": 1.0,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": "<"}
                    ).ref_id,
                    "comparison_attr_value": "1000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
            ],
        },
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 2,
            "factor_value": 0.9,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": "<"}
                    ).ref_id,
                    "comparison_attr_value": "5000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": ">="}
                    ).ref_id,
                    "comparison_attr_value": "1000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
            ],
        },
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 3,
            "factor_value": 0.8,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": ">="}
                    ).ref_id,
                    "comparison_attr_value": "5000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
            ],
        },
    ]


def DATA_SIC_CODE(provision: Model_ConfigProvision):
    return [
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 1,
            "factor_value": 0.82,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": "<"}
                    ).ref_id,
                    "comparison_attr_value": "5000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "string"}
                    ).ref_id,
                },
            ],
        },
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 2,
            "factor_value": 1.07,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": ">="}
                    ).ref_id,
                    "comparison_attr_value": "5000",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "string"}
                    ).ref_id,
                },
            ],
        },
    ]


def DATA_RED70(provision: Model_ConfigProvision):
    return [
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 1,
            "factor_value": 0.8,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": "="}
                    ).ref_id,
                    "comparison_attr_value": "true",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "boolean"}
                    ).ref_id,
                },
                {
                    "comparison_attr_name": "rate_table.age_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": ">="}
                    ).ref_id,
                    "comparison_attr_value": "65",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
            ],
        },
        {
            "config_provision_id": provision.config_provision_id,
            "factor_priority": 2,
            "factor_value": 0.92,
            "factor_rules": [
                {
                    "comparison_attr_name": "provision.selection_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": "="}
                    ).ref_id,
                    "comparison_attr_value": "true",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "boolean"}
                    ).ref_id,
                },
                {
                    "comparison_attr_name": "rate_table.age_value",
                    "comparison_operator_id": Model_RefComparisonOperator.find_one_by_attr(
                        {"ref_attr_symbol": ">="}
                    ).ref_id,
                    "comparison_attr_value": "60",
                    "comparison_attr_data_type_id": Model_RefDataTypes.find_one_by_attr(
                        {"ref_attr_code": "number"}
                    ).ref_id,
                },
            ],
        },
    ]


PROVISION_CODES = {
    "group_size": DATA_GROUP_SIZE,
    "sic_code": DATA_SIC_CODE,
    "reduction_at_70": DATA_RED70,
}


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    for prov_code, func in PROVISION_CODES.items():
        provision = PROVISION(product, prov_code)
        data = func(provision)
        url = urljoin(
            hostname,
            f"api/config/product/{product.config_product_id}/provision/{provision.config_provision_id}/factors",
        )
        res = requests.post(url, json=data, **kwargs)
        if not res.ok:
            raise Exception(res.text)
