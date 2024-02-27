from app.shared import BaseSchema

from ..models import Model_SelectionRatingMapperDetail


class Schema_SelectionRatingMapperDetail(BaseSchema):
    class Meta:
        model = Model_SelectionRatingMapperDetail
        load_instance = True
        include_relationships = True
        include_fk = True
