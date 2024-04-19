import requests
from requests.compat import urljoin
from ..models import (
    Model_ConfigProduct,
    Model_ConfigPlanDesignSet_Coverage,
)


def PRODUCT(product_code: str):
    return Model_ConfigProduct.find_one_by_attr(
        {
            "config_product_code": product_code,
        }
    )


def get_plan_designs(product_id: int):
    return Model_ConfigPlanDesignSet_Coverage.get_available_plan_designs(product_id)


def PRODUCT_PLAN_DESIGNS(product: Model_ConfigProduct):
    plan_designs = get_plan_designs(product.config_product_id)
    return [
        {
            "config_product_id": product.config_product_id,
            "config_plan_design_set_label": "Low",
            "config_plan_design_set_description": f"Low Plan for {product.config_product_label}",
            "plan_design_details": [
                {
                    "config_parent_type_code": "plan_design",
                    "config_plan_design_set_id": pd.config_plan_design_set_id,
                    "default_value": None,
                }
                for pd in plan_designs
                if pd.config_plan_design_set_label == "Low"
            ],
        },
        {
            "config_product_id": product.config_product_id,
            "config_plan_design_set_label": "High",
            "config_plan_design_set_description": f"High Plan for {product.config_product_label}",
            "plan_design_details": [
                {
                    "config_parent_type_code": "plan_design",
                    "config_plan_design_set_id": pd.config_plan_design_set_id,
                    "default_value": None,
                }
                for pd in plan_designs
                if pd.config_plan_design_set_label == "High"
            ],
        },
    ]


def load(hostname: str, *args, **kwargs) -> None:
    product = PRODUCT("CI21000")
    url = urljoin(
        hostname, f"api/config/product/{product.config_product_id}/plan-designs"
    )
    DATA = PRODUCT_PLAN_DESIGNS(product)
    res = requests.post(url, json=DATA, **kwargs)
    if not res.ok:
        raise Exception(res.text)
