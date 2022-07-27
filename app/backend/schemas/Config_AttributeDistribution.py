from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeDistribution

class Schema_ConfigAttributeDistribution(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistribution
        load_instance = True
        include_relationships=True
        include_fk=True
