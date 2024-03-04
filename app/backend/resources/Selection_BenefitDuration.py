from app.extensions import db
from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionBenefitDuration
from ..schemas import Schema_SelectionBenefitDuration


class CRUD_SelectionBenefitDuration(BaseSelectionCRUDResource):
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration()
    EVENT = "selection_benefit_duration"


class CRUD_SelectionBenefitDuration_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration(many=True)
    EVENT = "selection_benefit_duration"

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        benefit_id = kwargs.get("benefit_id")
        if benefit_id is None:
            raise Exception("Route must contain `benefit_id` parameter")

        db.session.query(cls.model).filter_by(selection_benefit_id=benefit_id).delete()
        return super().bulk_create(*args, **kwargs)
