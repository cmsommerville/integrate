import datetime
from marshmallow import Schema, fields, validates_schema, ValidationError
from sqlalchemy import func, and_, or_, desc
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError, AppValidationError
from app.shared.utils import system_temporal_hint
from ..models import (
    Model_ConfigBenefit,
    Model_ConfigBenefitAuth,
    Model_ConfigBenefitAuth_ACL,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitVariationState,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
    Model_SelectionPlan,
)
from ..schemas import Schema_SelectionBenefit, Schema_SelectionBenefitDuration


class RowNotFoundError(Exception):
    pass


class Schema_UpdateBenefit(Schema):
    selection_benefit_id = fields.Integer(required=True)
    selection_value = fields.Float(required=True)
    version_id = fields.String(required=True)


class Schema_InsertBenefit_Duration(Schema):
    config_benefit_duration_set_id = fields.Integer(required=True)
    config_benefit_duration_detail_id = fields.Integer(required=True)
    selection_factor = fields.Float(
        required=False, dump_only=True, attribute="config_benefit_duration_factor"
    )


class Schema_InsertBenefit(Schema):
    config_benefit_variation_state_id = fields.Integer(required=True)
    selection_value = fields.Float(required=True)
    duration_sets = fields.Nested(
        Schema_InsertBenefit_Duration, many=True, required=False
    )


class PolymorphicSchema:
    @classmethod
    def load(cls, data, **kwargs):
        """
        Validate that if the rate groups assigned to each benefit are defined on the product
        """
        if data.get("selection_benefit_id") is not None:
            return Schema_UpdateBenefit().load(data, **kwargs)
        elif data.get("config_benefit_variation_state_id") is not None:
            return Schema_InsertBenefit().load(data, **kwargs)
        else:
            raise ValidationError(
                "Either selection_benefit_id + version_id or config_benefit_variation_state_id must be provided"
            )


class Schema_RemoveBenefit(Schema):
    selection_benefit_id = fields.Integer(required=True)
    version_id = fields.String(required=True)


class Selection_RPC_Benefit:
    schema = Schema_SelectionBenefit()

    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

    def _qry_benefit_auth_temporal(self):
        """
        Get min/max/step values for benefits as of the time `t`
        """
        AUTH = Model_ConfigBenefitAuth
        ACL = Model_ConfigBenefitAuth_ACL

        row_number_column = (
            func.row_number()
            .over(
                partition_by=AUTH.config_benefit_id,
                order_by=desc(AUTH.priority),
            )
            .label("rn")
        )
        return (
            db.session.query(
                AUTH.config_benefit_id,
                AUTH.min_value,
                AUTH.max_value,
                AUTH.step_value,
                row_number_column,
            )
            .join(ACL, AUTH.config_benefit_auth_id == ACL.config_benefit_auth_id)
            .with_hint(AUTH, system_temporal_hint(self.t))
            .with_hint(ACL, system_temporal_hint(self.t))
            .subquery()
        )

    def validate_benefit_amounts(
        self,
        selection_value: float,
        config_benefit_variation_state_id: int = None,
        selection_benefit_id: int = None,
        *args,
        **kwargs,
    ):
        """
        Validate that the provided selection value adheres to the min/max/step values
        configured on the benefit record
        """
        AUTH = self._qry_benefit_auth_temporal()
        BVS = Model_ConfigBenefitVariationState
        BNFT = Model_ConfigBenefit
        SEL = Model_SelectionBenefit
        qry = (
            db.session.query(
                BNFT, AUTH.c.min_value, AUTH.c.max_value, AUTH.c.step_value
            )
            .join(BVS, BNFT.config_benefit_id == BVS.config_benefit_id)
            .join(AUTH, AUTH.c.config_benefit_id == BNFT.config_benefit_id)
            .with_hint(BNFT, system_temporal_hint(self.t))
            .with_hint(BVS, system_temporal_hint(self.t))
            .filter(AUTH.c.rn == 1)
        )

        if selection_benefit_id is not None:
            qry = qry.join(
                SEL,
                SEL.config_benefit_variation_state_id
                == BVS.config_benefit_variation_state_id,
            ).filter(SEL.selection_benefit_id == selection_benefit_id)
        elif config_benefit_variation_state_id is not None:
            qry = qry.filter(
                BVS.config_benefit_variation_state_id
                == config_benefit_variation_state_id
            )
        else:
            raise AppValidationError(
                "Either config_benefit_variation_state_id or selection_benefit_id must be provided"
            )
        config_benefit, min_value, max_value, step_value = qry.one_or_none()

        if not config_benefit:
            raise AppValidationError("Cannot find benefit")

        if float(min_value) > selection_value:
            raise AppValidationError(
                "Selection must be greater than minimum permissible value"
            )
        if float(max_value) < selection_value:
            raise AppValidationError(
                "Selection must be less than maximum permissible value"
            )
        if selection_value % float(step_value) != 0:
            raise AppValidationError(
                "Selection must be a multiple of the permissible step value"
            )

    def get_benefit_variation_state_mapper(
        self, config_benefit_variation_state_id: int, selection_plan_id: int
    ):
        """
        Returns a dictionary containing:
        - config_benefit_variation_state_id
        - config_benefit_id
        - config_coverage_id
        - selection_coverage_id [nullable]

        The key to the dictionary is the config_benefit_variation_state_id
        """
        BNFT = Model_ConfigBenefit
        BVS = Model_ConfigBenefitVariationState
        SCOV = Model_SelectionCoverage
        data = (
            db.session.query(
                BVS.config_benefit_variation_state_id,
                BVS.config_benefit_id,
                BNFT.config_coverage_id,
                SCOV.selection_coverage_id,
            )
            .select_from(BVS)
            .join(BNFT, BVS.config_benefit_id == BNFT.config_benefit_id)
            .join(
                SCOV,
                SCOV.config_coverage_id == BNFT.config_coverage_id,
                isouter=True,
            )
            .with_hint(BVS, system_temporal_hint(self.t))
            .with_hint(BNFT, system_temporal_hint(self.t))
            .filter(
                BVS.config_benefit_variation_state_id
                == config_benefit_variation_state_id,
                SCOV.selection_plan_id == selection_plan_id,
            )
            .one()
        )

        return {
            "config_benefit_variation_state_id": data.config_benefit_variation_state_id,
            "config_benefit_id": data.config_benefit_id,
            "config_coverage_id": data.config_coverage_id,
            "selection_coverage_id": data.selection_coverage_id,
        }

    def get_required_benefit_duration_set_ids(
        self,
        config_benefit_variation_state_id: int,
    ):
        """
        Get a list of required benefit duration set IDs for a given benefit variation state.

        This is used to validate that the required duration sets are provided in the payload.
        """
        BVS = Model_ConfigBenefitVariationState
        BDS = Model_ConfigBenefitDurationSet

        required_benefit_duration_sets = (
            db.session.query(BDS.config_benefit_duration_set_id)
            .select_from(BVS)
            .join(BDS, BVS.config_benefit_id == BDS.config_benefit_id)
            .with_hint(BVS, system_temporal_hint(self.t))
            .with_hint(BDS, system_temporal_hint(self.t))
            .filter(
                BVS.config_benefit_variation_state_id
                == config_benefit_variation_state_id
            )
            .all()
        )

        return [r for (r,) in required_benefit_duration_sets]

    def get_benefit_duration_details(self, duration_sets):
        """
        Get the benefit duration details for the provided duration sets.

        Query by the pair of detail and set IDs
        """
        if not duration_sets:
            return []
        BDD = Model_ConfigBenefitDurationDetail
        filters = [
            and_(
                BDD.config_benefit_duration_detail_id
                == item["config_benefit_duration_detail_id"],
                BDD.config_benefit_duration_set_id
                == item["config_benefit_duration_set_id"],
            )
            for item in duration_sets
        ]
        return (
            db.session.query(BDD)
            .with_hint(BDD, system_temporal_hint(self.t))
            .filter(or_(*filters))
            .all()
        )

    def create_benefit_durations(cls, validated_data):
        """
        Returns an array of instances of new selection benefit durations

        This validates that the required = provided duration sets.
        It also validates that the combinations of duration sets and duration details
        are valid.
        """
        required_benefit_duration_sets = cls.get_required_benefit_duration_set_ids(
            validated_data["config_benefit_variation_state_id"]
        )
        duration_sets = validated_data.get("duration_sets", [])
        provided_duration_set_ids = {
            item["config_benefit_duration_set_id"] for item in duration_sets
        }
        if set(required_benefit_duration_sets) != provided_duration_set_ids:
            req_diff = [
                str(i)
                for i in list(
                    set(required_benefit_duration_sets).difference(
                        provided_duration_set_ids
                    )
                )
            ]
            prov_diff = [
                str(i)
                for i in list(
                    provided_duration_set_ids.difference(
                        set(required_benefit_duration_sets)
                    )
                )
            ]
            raise ValidationError(
                f"Benefit duration sets ({', '.join(req_diff) or '-'}) are required but not provided. Benefit duration sets ({', '.join(prov_diff) or '-'}) are provided but not required."
            )

        validated_duration_details = cls.get_benefit_duration_details(duration_sets)
        validated_duration_set_ids = {
            item.config_benefit_duration_set_id for item in validated_duration_details
        }
        if set(required_benefit_duration_sets) != validated_duration_set_ids:
            raise ValidationError("Invalid duration sets provided")

        duration_detail_data = Schema_InsertBenefit_Duration(many=True).dump(
            validated_duration_details
        )
        return Schema_SelectionBenefitDuration(many=True).load(duration_detail_data)

    def insert(self, validated_data, plan_id):
        """
        This will insert a new benefit if the selection coverage ID already exists.

        Otherwise, it will create a new coverage and benefit.
        """

        # validate that the selection value adheres to configuration
        self.validate_benefit_amounts(
            selection_value=validated_data["selection_value"],
            config_benefit_variation_state_id=validated_data[
                "config_benefit_variation_state_id"
            ],
            t=self.t,
        )
        bvs_mapper = self.get_benefit_variation_state_mapper(
            validated_data["config_benefit_variation_state_id"], plan_id
        )
        # create benefit duration and benefit instances
        duration_sets = self.create_benefit_durations(validated_data)
        bnft = Model_SelectionBenefit(
            selection_plan_id=plan_id,
            config_benefit_variation_state_id=validated_data[
                "config_benefit_variation_state_id"
            ],
            selection_value=validated_data["selection_value"],
            duration_sets=duration_sets,
        )

        # selection coverage already exists (due to some other benefit in the coverage being selected)
        if bvs_mapper["selection_coverage_id"] is not None:
            bnft.selection_coverage_id = bvs_mapper["selection_coverage_id"]
            db.session.add(bnft)

        # selection coverage does not exist
        else:
            cvg = Model_SelectionCoverage(
                selection_plan_id=plan_id,
                config_coverage_id=bvs_mapper["config_coverage_id"],
            )
            cvg.benefits.append(bnft)
            db.session.add(cvg)
        db.session.flush()
        return bnft

    @classmethod
    def modify_errors(cls, validated_data, plan_id, *args, **kwargs):
        """
        Call this method to check if the version ID is expired or
        the benefit provided does not exist.
        """
        row_count = (
            db.session.query(Model_SelectionBenefit.selection_benefit_id)
            .filter_by(
                selection_plan_id=plan_id,
                selection_benefit_id=validated_data["selection_benefit_id"],
            )
            .count()
        )
        if row_count == 0:
            raise RowNotFoundError("Benefit does not exist")
        raise ExpiredRowVersionError(
            "The benefit you are trying to update has been modified by another user"
        )

    def update(self, validated_data, plan_id):
        # validate that the selection value adheres to configuration
        self.validate_benefit_amounts(
            selection_value=validated_data["selection_value"],
            selection_benefit_id=validated_data["selection_benefit_id"],
        )
        qry = Model_SelectionBenefit.query.filter_by(
            selection_plan_id=plan_id,
            selection_benefit_id=validated_data["selection_benefit_id"],
        )
        res = qry.filter_by(
            version_id=validated_data["version_id"],
        ).update({"selection_value": validated_data["selection_value"]})
        if res == 0:
            self.modify_errors(validated_data, plan_id)
        db.session.flush()
        return qry.first()

    @classmethod
    def delete(cls, validated_data, plan_id, *args, **kwargs):
        qry = Model_SelectionBenefit.query.filter_by(
            selection_plan_id=plan_id,
            selection_benefit_id=validated_data["selection_benefit_id"],
            version_id=validated_data["version_id"],
        )
        res = qry.delete()
        if res == 0:
            cls.modify_errors(validated_data, plan_id)
        db.session.flush()

    def upsert_benefit(self, *args, **kwargs):
        """
        Update the existing selection benefit if it exists, otherwise create a new one.
        """
        validated_data = PolymorphicSchema.load(self.payload)
        if validated_data.get("selection_benefit_id") is not None:
            obj = self.update(validated_data, self.plan_id)
        else:
            obj = self.insert(validated_data, self.plan_id)
        return self.schema.dump(obj)

    def remove_benefit(self, *args, **kwargs):
        validation_schema = Schema_RemoveBenefit()
        validated_data = validation_schema.load(self.payload)
        self.delete(validated_data, self.plan_id)
        return None
