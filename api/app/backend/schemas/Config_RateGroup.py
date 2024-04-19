from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRateGroup


class Schema_ConfigRateGroup(BaseSchema):
    class Meta:
        model = Model_ConfigRateGroup
        load_instance = True
        include_relationships = True
        include_fk = True
