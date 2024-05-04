import requests
from requests.compat import urljoin
from app.backend.models import (
    Model_ConfigProduct,
    Model_ConfigBenefitVariation,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_RefOptionality,
)


def PRODUCT_ID():
    return Model_ConfigProduct.find_one_by_attr(
        {"config_product_code": "CI21000"}
    ).config_product_id


def DATA_BENEFIT_COVARIANCE(product_id: int):
    return [
        {
            "config_benefit_product_variation_id": Model_ConfigBenefitVariation.find_one_by_attr(
                {
                    "config_benefit_id": Model_ConfigBenefit.find_one_by_attr(
                        {"config_benefit_version_code": "std_ms"}
                    ).config_benefit_id,
                    "config_product_variation_id": Model_ConfigProductVariation.find_one_by_attr(
                        {"config_product_variation_version_code": "std_issue_age"}
                    ).config_product_variation_id,
                }
            ).config_benefit_product_variation_id,
            "config_product_id": product_id,
            "ref_optionality_id": Model_RefOptionality.find_one_by_attr(
                {"ref_attr_code": "required"}
            ).ref_id,
            "covariance_details": [
                {
                    "config_benefit_product_variation_id": Model_ConfigBenefitVariation.find_one_by_attr(
                        {
                            "config_benefit_id": Model_ConfigBenefit.find_one_by_attr(
                                {"config_benefit_version_code": "std_als"}
                            ).config_benefit_id,
                            "config_product_variation_id": Model_ConfigProductVariation.find_one_by_attr(
                                {
                                    "config_product_variation_version_code": "std_issue_age"
                                }
                            ).config_product_variation_id,
                        }
                    ).config_benefit_product_variation_id,
                }
            ],
            "acl": [
                {"auth_role_code": "uw900"},
                {"auth_role_code": "uw1000"},
            ],
        },
        {
            "config_benefit_product_variation_id": Model_ConfigBenefitVariation.find_one_by_attr(
                {
                    "config_benefit_id": Model_ConfigBenefit.find_one_by_attr(
                        {"config_benefit_version_code": "std_als"}
                    ).config_benefit_id,
                    "config_product_variation_id": Model_ConfigProductVariation.find_one_by_attr(
                        {"config_product_variation_version_code": "std_issue_age"}
                    ).config_product_variation_id,
                }
            ).config_benefit_product_variation_id,
            "config_product_id": product_id,
            "ref_optionality_id": Model_RefOptionality.find_one_by_attr(
                {"ref_attr_code": "required"}
            ).ref_id,
            "covariance_details": [
                {
                    "config_benefit_product_variation_id": Model_ConfigBenefitVariation.find_one_by_attr(
                        {
                            "config_benefit_id": Model_ConfigBenefit.find_one_by_attr(
                                {"config_benefit_version_code": "std_ms"}
                            ).config_benefit_id,
                            "config_product_variation_id": Model_ConfigProductVariation.find_one_by_attr(
                                {
                                    "config_product_variation_version_code": "std_issue_age"
                                }
                            ).config_product_variation_id,
                        }
                    ).config_benefit_product_variation_id,
                }
            ],
            "acl": [
                {"auth_role_code": "uw900"},
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f"api/config/product/{product_id}/benefit-covariance/sets")
    res = requests.post(url, json=DATA_BENEFIT_COVARIANCE(product_id), **kwargs)
    if not res.ok:
        raise Exception(res.text)
