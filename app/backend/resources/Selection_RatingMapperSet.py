from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionRatingMapperSet
from ..schemas import Schema_SelectionRatingMapperSet


class CRUD_SelectionRatingMapperSet(BaseSelectionCRUDResource):
    model = Model_SelectionRatingMapperSet
    schema = Schema_SelectionRatingMapperSet()
    EVENT = "selection_rating_mapper_set"


class CRUD_SelectionRatingMapperSet_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionRatingMapperSet
    schema = Schema_SelectionRatingMapperSet(many=True)
    EVENT = "selection_rating_mapper_set"
