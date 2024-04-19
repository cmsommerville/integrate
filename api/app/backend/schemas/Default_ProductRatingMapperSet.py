from app.extensions import ma
from app.shared import BaseSchema

from ..models import (
    Model_DefaultProductRatingMapperSet,
)
from .Config_RatingMapperDetail import Schema_ConfigRatingMapperDetail


class Schema_DefaultProductRatingMapperSet(BaseSchema):
    class Meta:
        model = Model_DefaultProductRatingMapperSet
        load_instance = True
        include_relationships = True
        include_fk = True

    mapper_details = ma.Nested(Schema_ConfigRatingMapperDetail, many=True)


class Schema_DefaultProductRatingMapperDetail_For_Selection(ma.Schema):
    config_rating_mapper_detail_id = ma.Integer()
    rate_table_attribute_detail_id = ma.Integer()
    output_attribute_detail_id = ma.Integer()
    default_weight = ma.Method("get_default_weight", deserialize="load_default_weight")
    weight = ma.Float()

    def get_default_weight(self, obj):
        return float(obj.weight)

    def load_default_weight(self, val):
        return float(val)


class Schema_DefaultProductRatingMapperSet_For_Selection(ma.Schema):
    """
    This schema dumps the default product rating mapper set configured
    on the rating mapper collection into a format that can be loaded
    into the selection rating mapper set and detail.

    The pattern should be
    ```
    data = this_schema.dump(default_product_rating_mapper_set)
    selection_objs = selection_schema.load(data)
    ```
    """

    selection_plan_id = ma.Integer()
    config_rating_mapper_set_id = ma.Integer(
        attribute="default_config_rating_mapper_set_id"
    )
    selection_rating_mapper_set_type = ma.String()
    has_custom_weights = ma.Boolean(default=False)
    mapper_details = ma.Nested(
        Schema_DefaultProductRatingMapperDetail_For_Selection, many=True
    )
