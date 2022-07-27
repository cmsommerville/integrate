from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRelationshipMapperSet

class Schema_ConfigRelationshipMapperSet(BaseSchema):
    class Meta:
        model = Model_ConfigRelationshipMapperSet
        load_instance = True
        include_relationships=True
        include_fk=True
