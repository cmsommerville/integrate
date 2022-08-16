from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionCensusSet

class Schema_SelectionCensusSet(BaseSchema):
    class Meta:
        model = Model_SelectionCensusSet
        load_instance = True
        include_relationships=True
        include_fk=True
