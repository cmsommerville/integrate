from app.extensions import api, ma
from app.shared import BaseSchema
from flask_restx import fields

from ..models import Model_SelectionBenefit
from .Selection_BenefitDuration import Schema_SelectionBenefitDuration

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
        include_fk = True

    duration_sets = ma.Nested("Schema_SelectionBenefitDuration", many=True)
    # durations = ma.Method("get_benefit_durations", deserialize="load_benefit_durations")

    def get_benefit_durations(self, obj, *args, **kwargs):
        return Schema_SelectionBenefitDuration(context=self.context).dump(
            obj.get_benefit_durations(**self.context), many=True
        )

    def load_benefit_durations(self, value, *args, **kwargs):
        return [
            Schema_SelectionBenefitDuration(context=self.context).load(v) for v in value
        ]
