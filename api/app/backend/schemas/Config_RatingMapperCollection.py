from app.extensions import ma
from app.shared import BaseSchema
from marshmallow import Schema, fields

from ..models import Model_ConfigRatingMapperCollection
from .Config_AttributeSet import Schema_ConfigAttributeSet
from .Config_RatingMapperSet import (
    Schema_ConfigRatingMapperSet,
    Schema_ConfigRatingMapperSet_Dropdown,
)


class Schema_ConfigRatingMapperCollection(BaseSchema):
    class Meta:
        model = Model_ConfigRatingMapperCollection
        load_instance = True
        include_relationships = True
        include_fk = True

    attribute_set = ma.Nested(Schema_ConfigAttributeSet)
    mapper_sets = ma.Nested(Schema_ConfigRatingMapperSet, many=True)


class Schema_ConfigRatingMapperCollection_MapperSets(BaseSchema):
    config_rating_mapper_collection_id = fields.Int()
    config_rating_mapper_collection_label = fields.Str()
    is_selectable = fields.Bool()
    can_override_distribution = fields.Bool()
    default_config_rating_mapper_set = ma.Nested(Schema_ConfigRatingMapperSet_Dropdown)
    mapper_sets = ma.Nested(Schema_ConfigRatingMapperSet_Dropdown, many=True)
