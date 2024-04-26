import requests
from requests.compat import urljoin
from app.backend.models import (
    Model_ConfigCoverage,
    Model_ConfigProduct,
    Model_ConfigRateGroup,
    Model_RefUnitCode,
)


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def DATA_BENEFIT(product_id):
    return [
        {
            "config_product_id": product_id,
            "config_benefit_code": "cancer",
            "config_benefit_label": "Internal Cancer",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "heart_attack",
            "config_benefit_label": "Acute Myocardial Infarction",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "stroke",
            "config_benefit_label": "Stroke",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "renal_failure",
            "config_benefit_label": "End Stage Renal Failure",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "transplant",
            "config_benefit_label": "Major Organ Transplant",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "als",
            "config_benefit_label": "Amyotrophic Lateral Sclerosis",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "prog_benefits"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "ms",
            "config_benefit_label": "Multiple Sclerosis",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "prog_benefits"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "APU"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 25,
                    "step_value": 12.5,
                    "default_value": 25,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 12.5,
                    "default_value": 100,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "percent"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "wellness",
            "config_benefit_label": "Wellness Benefit",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "FLAT"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 50,
                    "step_value": 50,
                    "default_value": 50,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 100,
                    "step_value": 25,
                    "default_value": 50,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "dollars"}
            ).ref_id,
            "config_benefit_description": "",
        },
        {
            "config_product_id": product_id,
            "config_benefit_code": "skin_cancer",
            "config_benefit_label": "Skin Cancer",
            "config_coverage_id": Model_ConfigCoverage.find_one_by_attr(
                {"config_coverage_code": "base"}
            ).config_coverage_id,
            "config_rate_group_id": Model_ConfigRateGroup.find_one_by_attr(
                {"config_rate_group_code": "FLAT"}
            ).config_rate_group_id,
            "benefit_auth": [
                {
                    "priority": 10,
                    "min_value": 0,
                    "max_value": 500,
                    "step_value": 250,
                    "default_value": 500,
                    "acl": [{"auth_role_code": "uw900"}],
                },
                {
                    "priority": 20,
                    "min_value": 0,
                    "max_value": 1000,
                    "step_value": 50,
                    "default_value": 500,
                    "acl": [{"auth_role_code": "uw1000"}],
                },
            ],
            "unit_type_id": Model_RefUnitCode.find_one_by_attr(
                {"ref_attr_code": "dollars"}
            ).ref_id,
            "config_benefit_description": "",
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/benefits")
    res = requests.post(url, json=DATA_BENEFIT(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
