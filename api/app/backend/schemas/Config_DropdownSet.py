from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigDropdownSet
from .Config_DropdownDetail import Schema_ConfigDropdownDetail


class Schema_ConfigDropdownSet(BaseSchema):
    class Meta:
        model = Model_ConfigDropdownSet
        load_instance = True
        include_relationships = True
        include_fk = True

    dropdown_details = ma.Nested(Schema_ConfigDropdownDetail, many=True)
