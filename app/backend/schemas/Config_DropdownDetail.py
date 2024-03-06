from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigDropdownDetail


class Schema_ConfigDropdownDetail(BaseSchema):
    class Meta:
        model = Model_ConfigDropdownDetail
        load_instance = True
        include_relationships = True
        include_fk = True
