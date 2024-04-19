from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitProvision

class Schema_ConfigBenefitProvision(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitProvision
        load_instance = True
        include_relationships=True
        include_fk=True