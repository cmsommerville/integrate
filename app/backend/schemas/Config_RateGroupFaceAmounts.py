from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRateGroupFaceAmounts

class Schema_ConfigRateGroupFaceAmounts(BaseSchema):
    class Meta:
        model = Model_ConfigRateGroupFaceAmounts
        load_instance = True
        include_relationships=True
        include_fk=True
