from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAgeDistributionSet
from .Config_AgeDistribution import Schema_ConfigAgeDistribution

class Schema_ConfigAgeDistributionSet(BaseSchema):
    class Meta:
        model = Model_ConfigAgeDistributionSet
        load_instance = True
        include_relationships=True
        include_fk=True
        
    age_distribution = ma.Nested(Schema_ConfigAgeDistribution, many=True)