from app.extensions import ma
from app.shared import BaseSchema

from .. import models
from .Config_PlanDesignSet import (
    Schema_ConfigPlanDesignSet_Product,
    Schema_ConfigPlanDesignSet_Coverage,
)


class Schema_ConfigPlanDesignVariationState(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignVariationState
        load_instance = True
        include_fk = True


class Schema_ConfigPlanDesignVariationState_CoveragePlanDesignList(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignVariationState
        load_instance = True
        include_fk = True

    plan_design_sets = ma.Nested(Schema_ConfigPlanDesignSet_Coverage, many=True)


class Schema_ConfigPlanDesignVariationState_ProductPlanDesignList(BaseSchema):
    class Meta:
        model = models.Model_ConfigPlanDesignVariationState
        load_instance = True
        include_fk = True

    plan_design_sets = ma.Nested(Schema_ConfigPlanDesignSet_Product, many=True)
