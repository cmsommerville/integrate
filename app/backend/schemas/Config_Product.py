from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProduct
from .Config_AttributeSet import Schema_ConfigAttributeSet_Gender, Schema_ConfigAttributeSet_SmokerStatus
from .Ref_Master import Schema_RefRatingStrategy

class Schema_ConfigProduct(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships=True
        include_fk=True

    gender_attr_set = ma.Nested(Schema_ConfigAttributeSet_Gender)
    gender_rating_strategy = ma.Nested(Schema_RefRatingStrategy)

    smoker_status_attr_set = ma.Nested(Schema_ConfigAttributeSet_SmokerStatus)
    smoker_status_rating_strategy = ma.Nested(Schema_RefRatingStrategy)

    age_rating_strategy = ma.Nested(Schema_RefRatingStrategy)