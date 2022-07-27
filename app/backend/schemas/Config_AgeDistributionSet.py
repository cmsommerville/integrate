from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeDistributionSet

class Schema_ConfigAgeDistributionSet(BaseSchema):
    class Meta:
        model = Model_ConfigAgeDistributionSet
        load_instance = True
        include_relationships=True
        include_fk=True
