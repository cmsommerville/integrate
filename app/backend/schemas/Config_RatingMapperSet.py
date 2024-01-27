from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRatingMapperSet


class Schema_ConfigRatingMapperSet(BaseSchema):
    class Meta:
        model = Model_ConfigRatingMapperSet
        load_instance = True
        include_relationships = True
        include_fk = True
