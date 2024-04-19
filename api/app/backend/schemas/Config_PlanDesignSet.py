from app.extensions import ma
from app.shared import BaseSchema

from .. import models
from .Config_PlanDesignDetail import (
    Schema_ConfigPlanDesignDetail_Benefit,
    Schema_ConfigPlanDesignDetail_PlanDesign,
)


class Schema_ConfigPlanDesignSet_Coverage(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignSet_Coverage
        load_instance = True

    config_parent_type_code = ma.Constant("coverage")
    config_parent_id = ma.Integer(data_key="config_coverage_id")

    plan_design_details = ma.Nested(Schema_ConfigPlanDesignDetail_Benefit, many=True)


class Schema_ConfigPlanDesignSet_Product(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignSet_Product
        load_instance = True

    config_parent_type_code = ma.Constant("product")
    config_parent_id = ma.Integer(data_key="config_product_id")

    plan_design_details = ma.Nested(
        Schema_ConfigPlanDesignDetail_PlanDesign, many=True, load_only=True
    )
    coverage_plan_designs = ma.Nested(
        Schema_ConfigPlanDesignSet_Coverage, many=True, dump_only=True
    )


class Schema_ConfigPlanDesignSet_AvailableProductPlanDesigns(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignSet_Product
        load_instance = True

    config_parent_type_code = ma.Constant("product")
    config_parent_id = ma.Integer(data_key="config_product_id")

    coverage_plan_designs = ma.Nested(Schema_ConfigPlanDesignSet_Coverage, many=True)
