from app.extensions import ma
from app.shared import BaseSchema

from .. import models


class Schema_ConfigPlanDesignDetail_Benefit(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignDetail_Benefit
        load_instance = True

    config_parent_type_code = ma.Constant("benefit")
    config_parent_id = ma.Integer(data_key="config_benefit_id")


class Schema_ConfigPlanDesignDetail_PlanDesign(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignDetail_PlanDesign
        load_instance = True

    config_parent_type_code = ma.Constant("plan_design")
    config_parent_id = ma.Integer(data_key="config_plan_design_set_id")
