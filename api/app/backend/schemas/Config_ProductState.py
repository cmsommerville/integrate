from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductState
from .Ref_States import Schema_RefStates

class Schema_ConfigProductState(BaseSchema):
    class Meta:
        model = Model_ConfigProductState
        load_instance = True
        include_relationships=True
        include_fk=True

    state = ma.Nested(Schema_RefStates(exclude=('svg_path',)), dump_only=True)