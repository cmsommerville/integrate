from app.extensions import ma
from marshmallow import Schema, fields
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitVariationState


class Schema_ConfigBenefitVariationState(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitVariationState
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigBenefitVariationStateRatesetUpdate_States(Schema):
    config_benefit_variation_state_id = fields.Int()
    version_id = fields.Str()


class Schema_ConfigBenefitVariationStateRatesetUpdate(Schema):
    config_rate_table_set_id = fields.Int()
    benefit_variation_states = ma.Nested(
        Schema_ConfigBenefitVariationStateRatesetUpdate_States, many=True
    )
