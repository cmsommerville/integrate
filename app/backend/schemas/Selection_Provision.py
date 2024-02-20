from app.shared import BaseSchema

from ..models import Model_SelectionProvision


class Schema_SelectionProvision(BaseSchema):
    class Meta:
        model = Model_SelectionProvision
        load_instance = True
        include_relationships = True
        include_fk = True
