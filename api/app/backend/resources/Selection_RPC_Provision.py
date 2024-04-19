from typing import List
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError, AppValidationError
from app.shared.utils import system_temporal_hint
from ..classes import FactorRulesetApplicator
from ..models import (
    Model_SelectionPlan,
    Model_SelectionProvision,
    Model_SelectionFactor,
    Model_ConfigProvision,
    Model_ConfigProvisionState,
    Model_ConfigFactorSet,
    Model_ConfigFactor,
)
from ..schemas import Schema_SelectionProvision


class RowNotFoundError(Exception):
    pass


class Schema_UpdateProvision(Schema):
    selection_provision_id = fields.Int(required=True)
    version_id = fields.Str(required=True)
    selection_value = fields.Str(required=True)


class Selection_RPC_Provision(FactorRulesetApplicator):
    schema = Schema_SelectionProvision()

    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.validated_data = Schema_UpdateProvision().load(payload)
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

    @classmethod
    def modify_errors(cls, validated_data, plan_id, *args, **kwargs):
        """
        Call this method to check if the version ID is expired or
        the benefit provided does not exist.
        """
        row_count = (
            db.session.query(Model_SelectionProvision.selection_provision_id)
            .filter_by(
                selection_plan_id=plan_id,
                selection_provision_id=validated_data["selection_provision_id"],
            )
            .count()
        )
        if row_count == 0:
            raise RowNotFoundError("Benefit does not exist")
        raise ExpiredRowVersionError(
            "The benefit you are trying to update has been modified by another user"
        )

    @classmethod
    def _update(cls, payload, plan_id, *args, **kwargs):
        res = (
            db.session.query(Model_SelectionProvision)
            .filter_by(
                selection_plan_id=plan_id,
                selection_provision_id=payload["selection_provision_id"],
                version_id=payload["version_id"],
            )
            .update(
                {"selection_value": payload["selection_value"]},
                synchronize_session="fetch",
            )
        )
        db.session.flush()
        if res == 0:
            cls.modify_errors(payload, plan_id)
        return Model_SelectionProvision.query.get(payload["selection_provision_id"])

    def update_provision(self, *args, **kwargs):
        """
        Update the provision selection. Then pull the config factors as of time `t`.
        Reapply the factor rulesets based on the new selection value.
        """
        selection_provision = self._update(self.validated_data, self.plan_id)
        config_factor_sets = self.get_config_factors(selection_provision, t=self.t)

        # get the selection factor set and factor values
        selection_factor_list = self.get_first_valid_ruleset(
            config_factor_sets, selection_provision, t=self.t
        )

        # if no match, clear factors and set factor set to NULL
        if selection_factor_list is None:
            selection_provision.selection_factor_set_id = None
            selection_provision.factors = []
            db.session.flush()
            return self.schema.dump(selection_provision)

        # handle happy path
        # important to delete the child selection factors first, flush transaction
        # then set to the correct values
        selection_provision.factors = []
        db.session.flush()

        selection_provision.factors = selection_factor_list
        db.session.flush()
        return self.schema.dump(selection_provision)
