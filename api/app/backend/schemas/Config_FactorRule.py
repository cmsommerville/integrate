from app.extensions import ma
from app.shared import BaseSchema, PrimitiveField

from ..models import Model_ConfigFactorRule

class Schema_ConfigFactorRule(BaseSchema):
    class Meta:
        model = Model_ConfigFactorRule
        load_instance = True
        include_relationships=True
        include_fk=True
