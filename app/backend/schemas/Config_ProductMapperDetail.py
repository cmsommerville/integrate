from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductMapperDetail

class Schema_ConfigProductMapperDetail(BaseSchema):
    class Meta:
        model = Model_ConfigProductMapperDetail
        load_instance = True
        include_relationships=True
        include_fk=True
