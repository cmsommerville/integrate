from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionPlan
from .Selection_CensusSet import Schema_SelectionCensusSet
from .Config_ProductMapperSet import Schema_ConfigProductMapperSet_Gender, Schema_ConfigProductMapperSet_SmokerStatus

class Schema_SelectionPlan(BaseSchema):
    class Meta:
        model = Model_SelectionPlan
        load_instance = True
        include_relationships=True
        include_fk=True
        
    census_set = ma.Nested(Schema_SelectionCensusSet(exclude=('census_details',)), dump_only=True)
    gender_mapper_set = ma.Nested(Schema_ConfigProductMapperSet_Gender(exclude=('mappers',)), dump_only=True)
    smoker_status_mapper_set = ma.Nested(Schema_ConfigProductMapperSet_SmokerStatus(exclude=('mappers',)), dump_only=True)