from app.shared import BaseSchema

from ..models import Model_ConfigProvision


class Schema_ConfigProvision(BaseSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships = True
        include_fk = True
