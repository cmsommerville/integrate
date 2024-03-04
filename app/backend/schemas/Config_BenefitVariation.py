from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitVariation
from .Config_BenefitVariationState import Schema_ConfigBenefitVariationState


class Schema_ConfigBenefitVariation(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitVariation
        load_instance = True
        include_relationships = True
        include_fk = True

    states = ma.Nested(Schema_ConfigBenefitVariationState, many=True)
