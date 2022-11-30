from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitDurationSet
from .Config_BenefitDurationDetail import Schema_ConfigBenefitDurationDetail

class Schema_ConfigBenefitDurationSet(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationSet
        load_instance = True
        include_relationships=True
        include_fk=True

    duration_items = ma.Nested(Schema_ConfigBenefitDurationDetail, many=True)
