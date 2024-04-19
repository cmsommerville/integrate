from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_RefStates

class Schema_RefStates(BaseSchema):
    class Meta:
        model = Model_RefStates
        load_instance = True
        include_relationships=True
        include_fk=True
