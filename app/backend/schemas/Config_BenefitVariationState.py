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


class Schema_ConfigBenefitVariationState_QuotableBenefits(Schema):
    config_benefit_variation_state_id = fields.Function(
        lambda obj: obj[0].config_benefit_variation_state_id
    )
    config_benefit_variation_id = fields.Function(
        lambda obj: obj[0].config_benefit_variation_id
    )
    config_benefit_id = fields.Function(lambda obj: obj[1].config_benefit_id)
    config_benefit_variation_state_effective_date = fields.Function(
        lambda obj: str(obj[0].config_benefit_variation_state_effective_date)
    )
    config_benefit_variation_state_expiration_date = fields.Function(
        lambda obj: str(obj[0].config_benefit_variation_state_expiration_date)
    )

    min_value = fields.Function(lambda obj: float(obj[1].min_value))
    max_value = fields.Function(lambda obj: float(obj[1].max_value))
    step_value = fields.Function(lambda obj: float(obj[1].step_value))
    default_value = fields.Function(lambda obj: float(obj[1].default_value))


class Schema_ConfigBenefitVariationStateRatesetUpdate_States(Schema):
    config_benefit_variation_state_id = fields.Int()
    version_id = fields.Str()


class Schema_ConfigBenefitVariationStateRatesetUpdate(Schema):
    config_rate_table_set_id = fields.Int()
    benefit_variation_states = ma.Nested(
        Schema_ConfigBenefitVariationStateRatesetUpdate_States, many=True
    )
