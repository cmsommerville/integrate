from app.extensions import api
from app.shared import BaseSchema
from flask_restx import fields

from ..models import Model_SelectionBenefit

APISchema_SelectionBenefit = api.model(
    "APISchema_SelectionBenefit",
    {
        "selection_benefit_id": fields.Integer(required=False),
        "selection_plan_id": fields.Integer(required=True),
        "config_benefit_variation_state_id": fields.Integer(required=True),
        "selection_value": fields.Float(required=True),
    },
)
APISchema_SelectionBenefit_Payload = api.model(
    "APISchema_SelectionBenefit_Payload",
    {
        "config_plan_design_set_id": fields.Integer(required=False),
        "data": fields.Nested(APISchema_SelectionBenefit, required=True),
    },
)

APISchema_SelectionBenefit_ListPayload = api.model(
    "APISchema_SelectionBenefit_ListPayload",
    {
        "config_plan_design_set_id": fields.Integer(required=False),
        "data": fields.List(fields.Nested(APISchema_SelectionBenefit), required=True),
    },
)


class Schema_SelectionBenefit(BaseSchema):
    class Meta:
        model = Model_SelectionBenefit
        load_instance = True
        include_relationships = True
        include_fk = True
