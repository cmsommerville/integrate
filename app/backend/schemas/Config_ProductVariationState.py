from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductVariationState

class Schema_ConfigProductVariationState(BaseSchema):
    class Meta:
        model = Model_ConfigProductVariationState
        load_instance = True
        include_relationships=True
        include_fk=True
