from flask import request
from flask_restx import Resource
from marshmallow import fields, Schema
from app.extensions import db
from ..models import (
    Model_SelectionBenefit,
    Model_SelectionPlan,
)
from .Selection_Dropdown_Benefit import Temporal_ConfigBenefitVariationState


class Schema_Getter_ConfigBenefitDurationDetail_SelectionPlan(Schema):
    config_benefit_duration_detail_id = fields.Integer()
    config_benefit_duration_detail_code = fields.String()
    config_benefit_duration_detail_label = fields.String()
    config_benefit_duration_factor = fields.Float()


class Schema_Getter_ConfigBenefitDurationSet_SelectionPlan(Schema):
    config_benefit_duration_set_id = fields.Integer()
    config_benefit_duration_set_code = fields.String()
    config_benefit_duration_set_label = fields.String()
    duration_items = fields.Nested(
        Schema_Getter_ConfigBenefitDurationDetail_SelectionPlan,
        many=True,
        attribute="_duration_items",
    )


class Schema_Getter_ConfigBenefits_SelectionPlan(Schema):
    config_benefit_variation_state_id = fields.Function(
        lambda obj: obj[0].config_benefit_variation_state_id
    )
    config_product_variation_state_id = fields.Function(
        lambda obj: obj[0].config_product_variation_state_id
    )
    config_benefit_id = fields.Function(lambda obj: obj[0].config_benefit_id)
    config_benefit_variation_state_effective_date = fields.Function(
        lambda obj: str(obj[0].config_benefit_variation_state_effective_date)
    )
    config_benefit_variation_state_expiration_date = fields.Function(
        lambda obj: str(obj[0].config_benefit_variation_state_expiration_date)
    )

    config_benefit_code = fields.Function(lambda obj: obj[1].config_benefit_code)
    config_benefit_label = fields.Function(lambda obj: obj[1].config_benefit_label)

    min_value = fields.Function(lambda obj: float(obj[2]))
    max_value = fields.Function(lambda obj: float(obj[3]))
    step_value = fields.Function(lambda obj: float(obj[4]))
    durations = fields.Function(
        lambda obj: Schema_Getter_ConfigBenefitDurationSet_SelectionPlan(
            many=True
        ).dump(obj[5])
    )


class Getter_ConfigBenefits_SelectionPlan(Resource):
    def get_plan(self, selection_plan_id: int, *args, **kwargs):
        """
        Get the selection plan with the given ID
        """
        SP = Model_SelectionPlan
        return (
            db.session.query(SP)
            .filter_by(selection_plan_id=selection_plan_id)
            .one_or_none()
        )

    def get(self, selection_plan_id: int, *args, **kwargs):
        """
        Get the configured benefits available at the time the selection plan was created
        """
        plan = self.get_plan(selection_plan_id)
        parent_subquery = (
            db.session.query(Model_SelectionBenefit)
            .filter_by(selection_plan_id=selection_plan_id)
            .subquery()
        )
        benefits = Temporal_ConfigBenefitVariationState.query(
            plan.plan_as_of_dts, parent_subquery
        )
        schema = Schema_Getter_ConfigBenefits_SelectionPlan(many=True)
        return schema.dump(benefits), 200
