from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRelationshipMapperDetail

class Schema_ConfigRelationshipMapperDetail(BaseSchema):
    class Meta:
        model = Model_ConfigRelationshipMapperDetail
        load_instance = True
        include_relationships=True
        include_fk=True
