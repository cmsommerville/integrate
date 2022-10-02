from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductMapperSet_Gender, Model_ConfigProductMapperSet_SmokerStatus
from .Config_ProductMapperDetail import Schema_ConfigProductMapperDetail

class Schema_ConfigProductMapperSet_Gender(BaseSchema):
    class Meta:
        model = Model_ConfigProductMapperSet_Gender
        load_instance = True
        include_relationships=True
        include_fk=True

    config_attr_type_code = ma.Constant('gender')
    mappers = ma.Nested(Schema_ConfigProductMapperDetail, many=True)
    mapper_type_label = ma.Function(lambda obj: obj.mapper_type.ref_attr_label)


class Schema_ConfigProductMapperSet_SmokerStatus(BaseSchema):
    class Meta:
        model = Model_ConfigProductMapperSet_SmokerStatus
        load_instance = True
        include_relationships=True
        include_fk=True

    config_attr_type_code = ma.Constant('smoker_status')
    mappers = ma.Nested(Schema_ConfigProductMapperDetail, many=True)
    mapper_type_label = ma.Function(lambda obj: obj.mapper_type.ref_attr_label)