from app.extensions import db
from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionBenefit
from ..schemas import Schema_SelectionBenefit
from ..validators.Selection_Benefit import (
    Validator_SelectionBenefit,
    Validator_SelectionBenefitList,
)


class CRUD_SelectionBenefit(BaseSelectionCRUDResource):
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit()
    EVENT = "selection_benefit"
    validator = Validator_SelectionBenefit


class CRUD_SelectionBenefit_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit(many=True)
    EVENT = "selection_benefit"
    validator = Validator_SelectionBenefitList

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        plan_id = kwargs.get("plan_id")
        if plan_id is None:
            raise Exception("Route must contain `plan_id` parameter")

        db.session.query(cls.model).filter_by(selection_plan_id=plan_id).delete()
        return super().bulk_create(*args, **kwargs)
