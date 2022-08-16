from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionCensusDetail

class Schema_SelectionCensusDetail(BaseSchema):
    class Meta:
        model = Model_SelectionCensusDetail
        load_instance = True
        include_relationships=True
        include_fk=True
