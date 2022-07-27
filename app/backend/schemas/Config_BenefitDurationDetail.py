from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitDurationDetail

class Schema_ConfigBenefitDurationDetail(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationDetail
        load_instance = True
        include_relationships=True
        include_fk=True
