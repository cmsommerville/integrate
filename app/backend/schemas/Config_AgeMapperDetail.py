from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeMapperDetail

class Schema_ConfigAgeMapperDetail(BaseSchema):
    class Meta:
        model = Model_ConfigAgeMapperDetail
        load_instance = True
        include_relationships=True
        include_fk=True
