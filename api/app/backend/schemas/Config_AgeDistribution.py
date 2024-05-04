from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeDistribution

class Schema_ConfigAgeDistribution(BaseSchema):
    class Meta:
        model = Model_ConfigAgeDistribution
        load_instance = True
        include_relationships=True
        include_fk=True
