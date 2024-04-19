from app.shared import BaseSchema

from ..models import Model_SelectionRatingMapperSet


class Schema_SelectionRatingMapperSet(BaseSchema):
    class Meta:
        model = Model_SelectionRatingMapperSet
        load_instance = True
        include_relationships = True
        include_fk = True
