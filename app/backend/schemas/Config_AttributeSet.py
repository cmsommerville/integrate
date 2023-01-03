from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigAttributeSet_Gender, \
    Model_ConfigAttributeSet_SmokerStatus, Model_ConfigAttributeSet_Relationship, \
    Model_ConfigAttributeSet, Model_ConfigAttributeSet_NoJoin
from .Config_AttributeDetail import Schema_ConfigAttributeDetail

class Schema_ConfigAttributeSet(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet
        load_instance = True
        include_relationships=True


class Schema_ConfigAttributeSet_Gender(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet_Gender
        load_instance = True
        include_relationships=True

    config_attr_type_code = ma.Constant('gender')
    attributes = ma.Nested(Schema_ConfigAttributeDetail, many=True)


class Schema_ConfigAttributeSet_SmokerStatus(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet_SmokerStatus
        load_instance = True
        include_relationships=True

    config_attr_type_code = ma.Constant('smoker_status')
    attributes = ma.Nested(Schema_ConfigAttributeDetail, many=True)


class Schema_ConfigAttributeSet_Relationship(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet_Relationship
        load_instance = True
        include_relationships=True

    config_attr_type_code = ma.Constant('relationship')
    attributes = ma.Nested(Schema_ConfigAttributeDetail, many=True)


class Schema_ConfigAttributeSet_NoJoin(BaseSchema):
    class Meta:
        model = Model_ConfigAttributeSet_NoJoin
        load_instance = True
        include_relationships=True

    config_attr_type_code = ma.Constant('__nojoin__')
    attributes = ma.Nested(Schema_ConfigAttributeDetail, many=True)
