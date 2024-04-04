from marshmallow import Schema, fields, ValidationError
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError, AppValidationError
from ..models import (
    Model_SelectionProvision,
    Model_SelectionFactor,
    Model_ConfigProvision,
    Model_ConfigFactor,
)
from ..schemas import Schema_SelectionProvision


class RowNotFoundError(Exception):
    pass


class Schema_UpdateProvision(Schema):
    selection_provision_id = fields.Int(required=True)
    version_id = fields.Int(required=True)
    selection_value = fields.Str(required=True)


class Selection_RPC_Provision:
    schema = Schema_SelectionProvision()

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

    @staticmethod
    def config_to_selection_factor(
        config_factor: Model_ConfigFactor, selection_provision_id: int
    ):
        return Model_SelectionFactor(
            selection_provision_id=selection_provision_id,
            config_factor_set_id=config_factor.config_factor_set_id,
            config_factor_id=config_factor.config_factor_id,
            selection_rate_table_age_value=config_factor.rate_table_age_value,
            selection_rating_attr_id1=config_factor.rating_attr_id1,
            selection_rating_attr_id2=config_factor.rating_attr_id2,
            selection_rating_attr_id3=config_factor.rating_attr_id3,
            selection_rating_attr_id4=config_factor.rating_attr_id4,
            selection_rating_attr_id5=config_factor.rating_attr_id5,
            selection_rating_attr_id6=config_factor.rating_attr_id6,
            selection_factor_value=config_factor.factor_value,
        )

    @classmethod
    def get_config_provision_with_factors(
        cls, selection_provision: Model_SelectionProvision
    ):
        return (
            db.session.query(Model_ConfigProvision)
            .options(joinedload(Model_ConfigProvision.factors))
            .filter_by(
                config_provision_id=selection_provision.config_provision.config_provision_id
            )
            .all()
        )

    @classmethod
    def get_first_valid_ruleset(
        cls,
        config_provision: Model_ConfigProvision,
        selection_provision: Model_SelectionProvision,
    ):
        # find first ruleset
        validated_factor_ruleset = next(
            (
                ruleset
                for ruleset in config_provision.factors
                if ruleset.apply_ruleset(selection_provision)
            ),
            None,
        )

        if validated_factor_ruleset is None:
            return []

        return [
            cls.config_to_selection_factor(
                val, selection_provision.selection_provision_id
            )
            for val in validated_factor_ruleset.factor_values
        ]

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

    @classmethod
    def update_provision(cls, payload, plan_id, *args, **kwargs):
        validated_payload = cls.schema.load(payload)
        selection_provision = cls._update(validated_payload, plan_id)
        config_provision = cls.get_config_provision_with_factors(selection_provision)

        # get the selection factor set and factor values
        selection_factor_list = cls.get_first_valid_ruleset(
            config_provision, selection_provision
        )

        # if no match, clear factors and set factor set to NULL
        if selection_factor_list is None:
            selection_provision.selection_factor_set_id = None
            selection_provision.factors = []
            db.session.flush()
            return cls.schema.dump(selection_provision)

        # handle happy path
        # important to delete the child selection factors first, flush transaction
        # then set to the correct values
        selection_provision.factors = []
        db.session.flush()

        selection_provision.factors = selection_factor_list
        db.session.flush()
        return cls.schema.dump(selection_provision)
