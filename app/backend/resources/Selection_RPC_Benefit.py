from marshmallow import Schema, fields, validates_schema, ValidationError
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError
from ..models import (
    Model_ConfigBenefit,
    Model_ConfigBenefitVariationState,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
)
from ..schemas import (
    Schema_SelectionBenefit,
)


class RowNotFoundError(Exception):
    pass


class Schema_UpsertBenefit(Schema):
    selection_benefit_id = fields.Integer(required=False)
    config_benefit_variation_state_id = fields.Integer(required=False)
    selection_value = fields.Float(required=True)
    version_id = fields.String(required=False)

    @validates_schema
    def validate_update_or_insert(self, data, **kwargs):
        """
        Validate that if the rate groups assigned to each benefit are defined on the product
        """
        if (data.get("selection_benefit_id") is not None) and (
            data.get("version_id") is not None
        ):
            pass
        elif data.get("config_benefit_variation_state_id") is not None:
            pass
        else:
            raise ValidationError(
                "Either selection_benefit_id + version_id or config_benefit_variation_state_id must be provided"
            )


class Schema_RemoveBenefit(Schema):
    selection_benefit_id = fields.Integer(required=True)
    version_id = fields.String(required=True)


class Selection_RPC_Benefit:
    schema = Schema_SelectionBenefit()

    @classmethod
    def get_benefit_variation_state_mapper(
        cls, config_benefit_variation_state_id: int, selection_plan_id: int
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

    @classmethod
    def insert(cls, validated_data, plan_id):
        """
        This will insert a new benefit if the selection coverage ID already exists.

        Otherwise, it will create a new coverage and benefit.
        """
        try:
            bvs_mapper = cls.get_benefit_variation_state_mapper(
                validated_data["config_benefit_variation_state_id"], plan_id
            )
            bnft = Model_SelectionBenefit(
                selection_plan_id=plan_id,
                config_benefit_variation_state_id=validated_data[
                    "config_benefit_variation_state_id"
                ],
                selection_value=validated_data["selection_value"],
            )
            if bvs_mapper["selection_coverage_id"] is not None:
                # selection coverage already exists (due to some other benefit in the coverage being selected)
                bnft.selection_coverage_id = bvs_mapper["selection_coverage_id"]
                db.session.add(bnft)
            else:
                # selection coverage does not exist
                cvg = Model_SelectionCoverage(
                    selection_plan_id=plan_id,
                    config_coverage_id=bvs_mapper["config_coverage_id"],
                )
                cvg.benefits.append(bnft)
                db.session.add(cvg)
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            db.session.commit()
            return bnft

    @classmethod
    def modify_errors(cls, validated_data, plan_id, *args, **kwargs):
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

    @classmethod
    def update(cls, validated_data, plan_id):
        try:
            qry = Model_SelectionBenefit.query.filter_by(
                selection_plan_id=plan_id,
                selection_benefit_id=validated_data["selection_benefit_id"],
            )
            res = qry.filter_by(
                version_id=validated_data["version_id"],
            ).update({"selection_value": validated_data["selection_value"]})
            if res == 0:
                cls.modify_errors(validated_data, plan_id)
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            db.session.commit()
            return qry.first()

    @classmethod
    def delete(cls, validated_data, plan_id, *args, **kwargs):
        try:
            qry = Model_SelectionBenefit.query.filter_by(
                selection_plan_id=plan_id,
                selection_benefit_id=validated_data["selection_benefit_id"],
                version_id=validated_data["version_id"],
            )
            res = qry.delete()
            if res == 0:
                cls.modify_errors(validated_data, plan_id)
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            db.session.commit()

    @classmethod
    def upsert_benefit(cls, payload, plan_id, *args, **kwargs):
        """
        Update the existing selection benefit if it exists, otherwise create a new one.
        """
        validation_schema = Schema_UpsertBenefit()
        validated_data = validation_schema.load(payload)
        if validated_data.get("selection_benefit_id") is not None:
            obj = cls.update(validated_data, plan_id)
        else:
            obj = cls.insert(validated_data, plan_id)
        return cls.schema.dump(obj)

    @classmethod
    def remove_benefit(cls, payload, plan_id, *args, **kwargs):
        validation_schema = Schema_RemoveBenefit()
        validated_data = validation_schema.load(payload)
        cls.delete(validated_data, plan_id)
        return None
