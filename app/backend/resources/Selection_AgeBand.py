from app.extensions import db
from app.shared import BaseSelectionCRUDResourceList, BaseSelectionCRUDResource
from ..models import Model_SelectionAgeBand
from ..schemas import Schema_SelectionAgeBand


class CRUD_SelectionAgeBand(BaseSelectionCRUDResource):
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand()
    EVENT = "selection_age_band"


class CRUD_SelectionAgeBand_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand(many=True)
    EVENT = "selection_age_band"

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        plan_id = kwargs.get("plan_id")
        if plan_id is None:
            raise Exception("Route must contain `plan_id` parameter")

        db.session.query(cls.model).filter_by(selection_plan_id=plan_id).delete()
        return super().bulk_create(*args, **kwargs)
