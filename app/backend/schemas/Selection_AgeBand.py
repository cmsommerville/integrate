from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionAgeBand

class Schema_SelectionAgeBand(BaseSchema):
    class Meta:
        model = Model_SelectionAgeBand
        load_instance = True
        include_relationships=True
        include_fk=True
