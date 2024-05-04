from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeSet
from .Config_AttributeDetail import Schema_ConfigAttributeDetail


class Schema_ConfigAttributeSet(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet
        load_instance = True
        include_relationships = True
