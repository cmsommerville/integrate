from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitVariation


class Schema_ConfigBenefitVariation(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitVariation
        load_instance = True
        include_relationships = True
        include_fk = True
