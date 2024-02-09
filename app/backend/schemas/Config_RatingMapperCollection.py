from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRatingMapperCollection
from .Config_AttributeSet import Schema_ConfigAttributeSet
from .Config_RatingMapperSet import Schema_ConfigRatingMapperSet


class Schema_ConfigRatingMapperCollection(BaseSchema):
    class Meta:
        model = Model_ConfigRatingMapperCollection
        load_instance = True
        include_relationships = True
        include_fk = True

    attribute_set = ma.Nested(Schema_ConfigAttributeSet)
    mapper_sets = ma.Nested(Schema_ConfigRatingMapperSet, many=True)
