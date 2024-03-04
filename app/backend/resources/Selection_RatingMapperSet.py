from app.extensions import db
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

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        plan_id = kwargs.get("plan_id")
        if plan_id is None:
            raise Exception("Route must contain `plan_id` parameter")

        db.session.query(cls.model).filter_by(selection_plan_id=plan_id).delete()
        return super().bulk_create(*args, **kwargs)
