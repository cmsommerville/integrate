from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeBandDetail

class Schema_ConfigAgeBandDetail(BaseSchema):
    class Meta:
        model = Model_ConfigAgeBandDetail
        load_instance = True
        include_relationships=True
        include_fk=True
