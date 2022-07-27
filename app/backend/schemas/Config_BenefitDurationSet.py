from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitDurationSet

class Schema_ConfigBenefitDurationSet(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationSet
        load_instance = True
        include_relationships=True
        include_fk=True
