from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitState

class Schema_ConfigBenefitState(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitState
        load_instance = True
        include_relationships=True
        include_fk=True
