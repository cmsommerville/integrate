from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeDistributionSet_Gender, Model_ConfigAttributeDistributionSet_SmokerStatus

class Schema_ConfigAttributeDistributionSet_Gender(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistributionSet_Gender
        load_instance = True
        include_relationships=True
        include_fk=True

class Schema_ConfigAttributeDistributionSet_SmokerStatus(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeDistributionSet_SmokerStatus
        load_instance = True
        include_relationships=True
        include_fk=True