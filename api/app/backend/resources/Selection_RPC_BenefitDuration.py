from marshmallow import Schema, fields, ValidationError
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError
from app.shared.utils import system_temporal_hint
from ..models import (
    Model_ConfigBenefitDurationDetail,
    Model_SelectionBenefitDuration,
    Model_SelectionPlan,
)
from ..schemas import Schema_SelectionBenefitDuration


class RowNotFoundError(Exception):
    pass


class Schema_UpdateBenefitDuration(Schema):
    selection_benefit_duration_id = fields.Integer(required=True)
    config_benefit_duration_detail_id = fields.Integer(required=True)
    version_id = fields.String(required=True)


class Selection_RPC_BenefitDuration:
    schema = Schema_SelectionBenefitDuration()

    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

    @classmethod
    def modify_errors(cls, validated_data, *args, **kwargs):
        """
        Call this method to check if the version ID is expired or
        the benefit provided does not exist.
        """
        row_count = (
            db.session.query(
                Model_SelectionBenefitDuration.selection_benefit_duration_id
            )
            .filter_by(
                selection_benefit_duration_id=validated_data[
                    "selection_benefit_duration_id"
                ],
            )
            .count()
        )
        if row_count == 0:
            raise RowNotFoundError("Benefit does not exist")
        raise ExpiredRowVersionError(
            "The benefit you are trying to update has been modified by another user"
        )

    def get_duration_detail(
        self,
        selection_benefit_duration_id: int,
        config_benefit_duration_detail_id: int,
        *args,
        **kwargs,
    ):
        """
        This query returns the configured benefit duration detail instance.
        It validates that the configured benefit duration detail is a valid option for the duration set on the selected benefit duration.
        """
        BDD = Model_ConfigBenefitDurationDetail
        SBD = Model_SelectionBenefitDuration
        return (
            db.session.query(BDD)
            .select_from(SBD)
            .join(
                BDD,
                BDD.config_benefit_duration_set_id
                == SBD.config_benefit_duration_set_id,
            )
            .with_hint(BDD, system_temporal_hint(self.t))
            .filter(
                SBD.selection_benefit_duration_id == selection_benefit_duration_id,
                BDD.config_benefit_duration_detail_id
                == config_benefit_duration_detail_id,
            )
            .one()
        )

    def update_benefit_duration(self, *args, **kwargs):
        """
        Update the existing selection benefit if it exists, otherwise create a new one.
        """
        validated_data = Schema_UpdateBenefitDuration().load(self.payload)
        config_duration_detail = self.get_duration_detail(**validated_data)
        res = (
            db.session.query(Model_SelectionBenefitDuration)
            .filter_by(
                selection_benefit_duration_id=validated_data[
                    "selection_benefit_duration_id"
                ]
            )
            .update(
                {
                    "config_benefit_duration_detail_id": config_duration_detail.config_benefit_duration_detail_id,
                    "selection_factor": float(
                        config_duration_detail.config_benefit_duration_factor
                    ),
                }
            )
        )
        if res == 0:
            self.modify_errors(validated_data)
        if res > 1:
            raise ValidationError("Multiple rows updated")
        db.session.flush()
        obj = Model_SelectionBenefitDuration.query.get(
            validated_data["selection_benefit_duration_id"]
        )
        return self.schema.dump(obj)
