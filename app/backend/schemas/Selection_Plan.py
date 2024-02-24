from app.shared import BaseSchema

from ..models import Model_SelectionPlan


class Schema_SelectionPlan(BaseSchema):
    class Meta:
        model = Model_SelectionPlan
        load_instance = True
        include_relationships = True
        include_fk = True
