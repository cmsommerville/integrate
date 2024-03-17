from flask import request
from flask_restx import Resource, fields
from sqlalchemy import case
from app.auth import authorization_required
from app.extensions import db, api
from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import (
    Model_SelectionBenefit,
    Model_ConfigBenefitVariationState,
    Model_SelectionPlan,
)
from ..schemas import (
    Schema_SelectionBenefit,
)
from ..validators.Selection_Benefit import (
    Validator_SelectionBenefit,
    Validator_SelectionBenefitList,
)

APIModel_PATCH_SetPlanDesign = api.model(
    "PATCH_SelectionPlan_SetPlanDesign",
    {
        "config_plan_design_set_id": fields.Integer,
    },
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
