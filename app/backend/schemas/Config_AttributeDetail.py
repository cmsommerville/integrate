from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeDetail


class Schema_ConfigAttributeDetail(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDetail
        load_instance = True
        include_fk = True
