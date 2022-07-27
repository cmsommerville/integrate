from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeBandSet

class Schema_ConfigAgeBandSet(BaseSchema):
    class Meta:
        model = Model_ConfigAgeBandSet
        load_instance = True
        include_relationships=True
        include_fk=True
