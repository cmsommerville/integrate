from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProduct
from .Ref_Master import Schema_RefRatingStrategy


class Schema_ConfigProduct(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = (
            "states",
            "config_rate_groups",
        )

    age_rating_strategy = ma.Nested(Schema_RefRatingStrategy)
