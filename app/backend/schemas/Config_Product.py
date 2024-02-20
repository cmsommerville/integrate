from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProduct
from .Config_RatingMapperCollection import (
    Schema_ConfigRatingMapperCollection,
    Schema_ConfigRatingMapperCollection_MapperSets,
)


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


class Schema_ConfigProduct_RatingMapperCollections(BaseSchema):
    class Meta:
        model = Model_ConfigProduct
        load_instance = True
        include_relationships = True
        include_fk = True
        exclude = (
            "states",
            "config_rate_groups",
        )

    rating_mapper_collection1 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
    rating_mapper_collection2 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
    rating_mapper_collection3 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
    rating_mapper_collection4 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
    rating_mapper_collection5 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
    rating_mapper_collection6 = ma.Nested(
        Schema_ConfigRatingMapperCollection_MapperSets
    )
