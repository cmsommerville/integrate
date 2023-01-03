from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeDistributionSet_Gender, Model_ConfigAttributeDistributionSet_SmokerStatus
from .Config_AttributeDistribution import Schema_ConfigAttributeDistribution

class Schema_ConfigAttributeDistributionSet_Gender(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistributionSet_Gender
        load_instance = True
        include_relationships=True
        include_fk=True

    gender_distribution = ma.Nested(Schema_ConfigAttributeDistribution, many=True)

class Schema_ConfigAttributeDistributionSet_SmokerStatus(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistributionSet_SmokerStatus
        load_instance = True
        include_relationships=True
        include_fk=True

    smoker_status_distribution = ma.Nested(Schema_ConfigAttributeDistribution, many=True)