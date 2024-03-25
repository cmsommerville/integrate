from app.shared import BaseSchema

from ..models import Model_SelectionCoverage


class Schema_SelectionCoverage(BaseSchema):
    class Meta:
        model = Model_SelectionCoverage
        load_instance = True
        include_relationships = True
        include_fk = True
