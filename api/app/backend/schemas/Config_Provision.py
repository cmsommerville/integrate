from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvision
from .Config_DropdownSet import Schema_ConfigDropdownSet


class Schema_ConfigProvision(BaseSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships = True
        include_fk = True

    dropdown_set = ma.Nested(Schema_ConfigDropdownSet)
