import requests
from requests.compat import urljoin
from app.models import Model_ConfigCoverage, Model_ConfigBenefit, Model_ConfigProduct


def COVERAGE(product_code: str, coverage_code: str):
    return Model_ConfigCoverage.find_one_by_attr(
        {
            "config_coverage_code": coverage_code,
            "config_product_id": Model_ConfigProduct.find_one_by_attr(
                {"config_product_code": product_code}
            ).config_product_id,
        }
    )


def get_benefits(coverage_id: int):
    return Model_ConfigBenefit.find_all_by_attr({"config_coverage_id": coverage_id})


def COVERAGE_PLAN_DESIGNS(coverage: Model_ConfigCoverage):
    benefits = get_benefits(coverage.config_coverage_id)
    return [
        {
            "config_coverage_id": coverage.config_coverage_id,
            "config_plan_design_set_label": "Low",
            "config_plan_design_set_description": f"Low Plan for {coverage.config_coverage_label}",
            "plan_design_details": [
                {
                    "config_parent_type_code": "benefit",
                    "config_benefit_id": benefit.config_benefit_id,
                    "default_value": float(
                        min(benefit.min_value + benefit.step_value, benefit.max_value)
                    ),
                }
                for benefit in benefits
            ],
        },
        {
            "config_coverage_id": coverage.config_coverage_id,
            "config_plan_design_set_label": "High",
            "config_plan_design_set_description": f"High Plan for {coverage.config_coverage_label}",
            "plan_design_details": [
                {
                    "config_parent_type_code": "benefit",
                    "config_benefit_id": benefit.config_benefit_id,
                    "default_value": float(benefit.max_value),
                }
                for benefit in benefits
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    COVERAGE_CODES = ["base", "prog_benefits"]
    for covg_code in COVERAGE_CODES:
        coverage = COVERAGE("CI21000", covg_code)
        url = urljoin(
            hostname, f"api/config/coverage/{coverage.config_coverage_id}/plan-designs"
        )
        DATA = COVERAGE_PLAN_DESIGNS(coverage)
        res = requests.post(url, json=DATA, **kwargs)
        if not res.ok:
            raise Exception(res.text)
