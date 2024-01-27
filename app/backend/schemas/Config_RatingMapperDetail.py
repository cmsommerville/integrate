from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRatingMapperDetail


class Schema_ConfigRatingMapperDetail(BaseSchema):
    class Meta:
        model = Model_ConfigRatingMapperDetail
        load_instance = True
        include_relationships = True
        include_fk = True
