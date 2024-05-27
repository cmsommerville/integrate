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
    def list(cls, *args, **kwargs):
        if kwargs.get("parent_id") is not None:
            objs = cls.model.find_by_plan(kwargs.get("parent_id"))
        else:
            objs = cls.model.find_all(*args, **kwargs)
        return cls.schema.dump(objs)

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        parent_id = kwargs.get("parent_id")
        if parent_id is None:
            raise Exception("Route must contain `parent_id` parameter")

        db.session.query(cls.model).filter_by(selection_plan_id=parent_id).delete()
        return super().bulk_create(*args, **kwargs)
