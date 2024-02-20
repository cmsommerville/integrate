from app.extensions import ma
from app.shared import BaseSchema
from marshmallow import Schema, fields

from ..models import Model_ConfigRatingMapperSet


class Schema_ConfigRatingMapperSet(BaseSchema):
    class Meta:
        model = Model_ConfigRatingMapperSet
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigRatingMapperSet_Dropdown(Schema):
    config_rating_mapper_set_id = fields.Int()
    config_rating_mapper_set_label = fields.Str()
    is_composite = fields.Bool()
    is_employer_paid = fields.Bool()
