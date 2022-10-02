from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionRateGroupFaceAmounts

class Schema_SelectionRateGroupFaceAmounts(BaseSchema):
    class Meta:
        model = Model_SelectionRateGroupFaceAmounts
        load_instance = True
        include_relationships=True
        include_fk=True
    