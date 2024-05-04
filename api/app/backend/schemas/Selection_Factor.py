from marshmallow import fields, EXCLUDE
from app.shared import BaseSchema

from ..models import Model_SelectionFactor


class Schema_SelectionFactor(BaseSchema):
    class Meta:
        model = Model_SelectionFactor
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_SelectionFactorFromConfigFactor(BaseSchema):
    class Meta:
        model = Model_SelectionFactor
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    selection_rating_attr_id1 = fields.Int(data_key="rating_attr_id1")
    selection_rating_attr_id2 = fields.Int(data_key="rating_attr_id2")
    selection_rating_attr_id3 = fields.Int(data_key="rating_attr_id3")
    selection_rating_attr_id4 = fields.Int(data_key="rating_attr_id4")
    selection_rating_attr_id5 = fields.Int(data_key="rating_attr_id5")
    selection_rating_attr_id6 = fields.Int(data_key="rating_attr_id6")
