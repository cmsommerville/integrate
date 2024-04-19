from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigFactorSet, Model_ConfigFactor


class Schema_ConfigFactorSet(BaseSchema):
    class Meta:
        model = Model_ConfigFactorSet
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigFactor(BaseSchema):
    class Meta:
        model = Model_ConfigFactor
        load_instance = True
        include_relationships = True
        include_fk = True
