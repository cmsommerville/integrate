from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductVariation


class Schema_ConfigProductVariation(BaseSchema):
    class Meta:
        model = Model_ConfigProductVariation
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigProductVariation_SetPlanDesignVariationStates(ma.Schema):
    config_product_variation_state_id = ma.List(ma.Integer(required=True))
    config_plan_design_set_id = ma.List(ma.Integer(required=True))
