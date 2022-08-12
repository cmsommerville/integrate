from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProductMapperSet_Gender, Model_ConfigProductMapperSet_SmokerStatus

class Schema_ConfigProductMapperSet_Gender(BaseSchema):
    class Meta:
        model = Model_ConfigProductMapperSet_Gender
        load_instance = True
        include_relationships=True
        include_fk=True

    config_attr_type_code = ma.Constant('gender')


class Schema_ConfigProductMapperSet_SmokerStatus(BaseSchema):
    class Meta:
        model = Model_ConfigProductMapperSet_SmokerStatus
        load_instance = True
        include_relationships=True
        include_fk=True

    config_attr_type_code = ma.Constant('smoker_status')