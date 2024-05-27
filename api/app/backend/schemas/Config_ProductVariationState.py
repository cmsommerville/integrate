from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductVariationState


class Schema_ConfigProductVariationState(BaseSchema):
    class Meta:
        model = Model_ConfigProductVariationState
        load_instance = True
        include_relationships = True
        include_fk = True

    default_product_plan_design = ma.Nested(
        "Schema_ConfigPlanDesignSet_Product", dump_only=True
    )
    selectable_product_plan_designs = ma.Nested(
        "Schema_ConfigPlanDesignSet_Product", many=True, dump_only=True
    )


class Schema_Getter_ConfigProductVariationState_SelectionPlan(BaseSchema):
    config_product_variation_state_id = ma.Integer()
    config_product_variation_id = ma.Integer()
    config_product_variation_label = ma.String()
    state_id = ma.Integer(data_key="situs_state_id")
    state_code = ma.String()
    state_name = ma.String()
