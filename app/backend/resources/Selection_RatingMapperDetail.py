from app.extensions import db
from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionRatingMapperDetail
from ..schemas import Schema_SelectionRatingMapperDetail


class CRUD_SelectionRatingMapperDetail(BaseSelectionCRUDResource):
    model = Model_SelectionRatingMapperDetail
    schema = Schema_SelectionRatingMapperDetail()
    EVENT = "selection_rating_mapper_detail"


class CRUD_SelectionRatingMapperDetail_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionRatingMapperDetail
    schema = Schema_SelectionRatingMapperDetail(many=True)
    EVENT = "selection_rating_mapper_detail"

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
