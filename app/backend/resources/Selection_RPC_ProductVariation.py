import datetime
import pandas as pd
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.sql import and_
from app.extensions import db
from ..models import (
    Model_SelectionPlan,
    Model_SelectionBenefit,
    Model_ConfigBenefitVariationState,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProduct,
)
from ..schemas import Schema_SelectionPlan


class RowNotFoundError(Exception):
    pass


class Schema_UpdateProductVariation(Schema):
    config_product_variation_id = fields.Integer(required=True)


class Selection_RPC_ProductVariation:
    schema = Schema_SelectionPlan(exclude=("coverages",))

    @classmethod
    def _qry_benefit_mapper(
        cls,
        config_product_variation_id: int,
        plan: Model_SelectionPlan,
    ):
        """
        Returns a mapping table. The table is unique two ways:
        1. By config_benefit_variation_state_id
        2. By config_product_id, config_product_variation_id, config_benefit_id, state_id
        """
        BVS = Model_ConfigBenefitVariationState
        BNFT = Model_ConfigBenefit
        PVS = Model_ConfigProductVariationState
        PV = Model_ConfigProductVariation
        PROD = Model_ConfigProduct

        return (
            db.session.query(
                BVS.config_benefit_variation_state_id,
                PROD.config_product_id,
                PV.config_product_variation_id,
                BNFT.config_benefit_id,
                BVS.state_id,
            )
            .select_from(BVS)
            .join(BNFT, BNFT.config_benefit_id == BVS.config_benefit_id)
            .join(
                PVS,
                PVS.config_product_variation_state_id
                == BVS.config_product_variation_state_id,
            )
            .join(PV, PV.config_product_variation_id == PVS.config_product_variation_id)
            .join(PROD, PROD.config_product_id == PV.config_product_id)
            .with_hint(BVS, "FOR SYSTEM_TIME AS OF '2024-04-06 00:00:00'")
            .with_hint(BNFT, "FOR SYSTEM_TIME AS OF '2024-04-06 00:00:00'")
            .with_hint(PVS, "FOR SYSTEM_TIME AS OF '2024-04-06 00:00:00'")
            .with_hint(PV, "FOR SYSTEM_TIME AS OF '2024-04-06 00:00:00'")
            .with_hint(PROD, "FOR SYSTEM_TIME AS OF '2024-04-06 00:00:00'")
            .filter(
                PROD.config_product_id == plan.config_product_id,
                PV.config_product_variation_id == config_product_variation_id,
                BVS.config_benefit_variation_state_effective_date
                <= plan.selection_plan_effective_date,
                BVS.config_benefit_variation_state_expiration_date
                >= plan.selection_plan_effective_date,
                PVS.config_product_variation_state_effective_date
                <= plan.selection_plan_effective_date,
                PVS.config_product_variation_state_expiration_date
                >= plan.selection_plan_effective_date,
            )
            .subquery()
        )

    @classmethod
    def get_product_variation_state(
        cls, config_product_variation_id, plan: Model_SelectionPlan
    ):
        PVS = Model_ConfigProductVariationState
        return (
            db.session.query(PVS)
            .filter(
                PVS.config_product_variation_id == config_product_variation_id,
                PVS.state_id == plan.situs_state_id,
                PVS.config_product_variation_state_effective_date
                <= plan.selection_plan_effective_date,
                PVS.config_product_variation_state_expiration_date
                >= plan.selection_plan_effective_date,
            )
            .one()
        )

    @classmethod
    def available_benefit_handler(
        cls, from_config_product_variation_id, to_config_product_variation_id, plan
    ):
        SB = Model_SelectionBenefit

        FROM = cls._qry_benefit_mapper(from_config_product_variation_id, plan)
        TO = cls._qry_benefit_mapper(to_config_product_variation_id, plan)

        qry = (
            db.session.query(SB, TO.c.config_benefit_variation_state_id)
            .select_from(SB)
            .join(
                FROM,
                FROM.c.config_benefit_variation_state_id
                == SB.config_benefit_variation_state_id,
            )
            .join(
                TO,
                and_(
                    TO.c.config_product_id == FROM.c.config_product_id,
                    TO.c.config_benefit_id == FROM.c.config_benefit_id,
                    TO.c.state_id == FROM.c.state_id,
                ),
            )
            .filter(
                SB.selection_plan_id == plan.selection_plan_id,
            )
        )

        available_selection_benefits = qry.all()

        for bnft, new_bvs_id in available_selection_benefits:
            bnft.config_benefit_variation_state_id = new_bvs_id
            db.session.add(bnft)

        db.session.flush()

    @classmethod
    def unavailable_benefit_handler(
        cls, from_config_product_variation_id, to_config_product_variation_id, plan
    ):
        """
        This method handles the case where previously selected benefits are unavailable under the new product variation.
        """
        SB = Model_SelectionBenefit

        FROM = cls._qry_benefit_mapper(from_config_product_variation_id, plan)
        TO = cls._qry_benefit_mapper(to_config_product_variation_id, plan)

        unavailable_selection_benefits_qry = (
            db.session.query(SB)
            .select_from(SB)
            .join(
                FROM,
                FROM.c.config_benefit_variation_state_id
                == SB.config_benefit_variation_state_id,
            )
            .join(
                TO,
                and_(
                    TO.c.config_product_id == FROM.c.config_product_id,
                    TO.c.config_benefit_id == FROM.c.config_benefit_id,
                    TO.c.state_id == FROM.c.state_id,
                ),
                isouter=True,
            )
            .filter(
                SB.selection_plan_id == plan.selection_plan_id,
                TO.c.config_benefit_variation_state_id == None,
            )
        )

        unavailable_selection_benefits = unavailable_selection_benefits_qry.all()
        db.session.expunge_all()
        delete_ids = [
            bnft.selection_benefit_id for bnft in unavailable_selection_benefits
        ]

        db.session.query(SB).filter(SB.selection_benefit_id.in_(delete_ids)).delete()
        db.session.flush()

        return unavailable_selection_benefits

    @classmethod
    def validate(
        cls, from_config_product_variation_id, to_config_product_variation_id, plan
    ):
        if from_config_product_variation_id == to_config_product_variation_id:
            raise ValidationError(
                "Product variation already set to the requested value"
            )

        FROM = cls._qry_benefit_mapper(from_config_product_variation_id, plan)
        TO = cls._qry_benefit_mapper(to_config_product_variation_id, plan)

        df_from = pd.DataFrame(
            db.session.query(FROM.c.config_product_variation_id).distinct().all()
        )
        df_to = pd.DataFrame(
            db.session.query(TO.c.config_product_variation_id).distinct().all()
        )
        df = pd.concat([df_from, df_to], ignore_index=True)

        if df.empty:
            raise ValidationError("No benefits found for the given product variations")
        if df["config_product_variation_id"].unique().size != 2:
            raise ValidationError("Invalid product variation selection")

    @classmethod
    def update_product_variation(cls, payload, plan_id, *args, **kwargs):
        validated_data = Schema_UpdateProductVariation().load(payload)

        plan = Model_SelectionPlan.query.get(plan_id)
        if not plan:
            raise RowNotFoundError("Plan not found")

        from_config_product_variation_id = (
            plan.config_product_variation_state.config_product_variation_id
        )
        to_config_product_variation_id = validated_data["config_product_variation_id"]

        cls.validate(
            from_config_product_variation_id, to_config_product_variation_id, plan
        )

        cls.available_benefit_handler(
            from_config_product_variation_id, to_config_product_variation_id, plan
        )

        unavailable_benefits = cls.unavailable_benefit_handler(
            from_config_product_variation_id, to_config_product_variation_id, plan
        )

        new_product_variation_state = cls.get_product_variation_state(
            to_config_product_variation_id, plan
        )
        plan.config_product_variation_state_id = (
            new_product_variation_state.config_product_variation_state_id
        )
        db.session.add(plan)
        db.session.flush()
        return cls.schema.dump(plan)
