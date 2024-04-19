import datetime
import pandas as pd
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.sql import and_
from app.extensions import db
from app.shared.utils import system_temporal_hint
from app.shared.errors import RowNotFoundError
from ..models import (
    Model_SelectionPlan,
    Model_SelectionBenefit,
    Model_ConfigBenefitVariationState,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProduct,
)
from ..schemas import Schema_SelectionPlan, Schema_SelectionBenefit


class Schema_UpdateProductVariation(Schema):
    config_product_variation_id = fields.Integer(required=True)


class Selection_RPC_ProductVariation:
    schema = Schema_SelectionPlan(exclude=("coverages",))

    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

    @classmethod
    def _qry_benefit_mapper(
        cls,
        config_product_variation_id: int,
        plan: Model_SelectionPlan,
        t: datetime.datetime = None,
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

        qry = (
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
        )
        if t is not None:
            asof_hint = system_temporal_hint(t)
            qry = (
                qry.with_hint(BVS, asof_hint)
                .with_hint(BNFT, asof_hint)
                .with_hint(PVS, asof_hint)
                .with_hint(PV, asof_hint)
                .with_hint(PROD, asof_hint)
            )
        return qry.subquery()

    def get_product_variation_state(self, config_product_variation_id):
        PVS = Model_ConfigProductVariationState
        qry = db.session.query(PVS).filter(
            PVS.config_product_variation_id == config_product_variation_id,
            PVS.state_id == self.plan.situs_state_id,
            PVS.config_product_variation_state_effective_date
            <= self.plan.selection_plan_effective_date,
            PVS.config_product_variation_state_expiration_date
            >= self.plan.selection_plan_effective_date,
        )
        if self.t is not None:
            asof_hint = system_temporal_hint(self.t)
            qry = qry.with_hint(PVS, asof_hint)

        return qry.one()

    def available_benefit_handler(
        self,
        from_config_product_variation_id,
        to_config_product_variation_id,
    ):
        SB = Model_SelectionBenefit

        FROM = self._qry_benefit_mapper(
            from_config_product_variation_id, self.plan, self.t
        )
        TO = self._qry_benefit_mapper(to_config_product_variation_id, self.plan, self.t)

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
                SB.selection_plan_id == self.plan.selection_plan_id,
            )
        )

        available_selection_benefits = qry.all()

        for bnft, new_bvs_id in available_selection_benefits:
            bnft.config_benefit_variation_state_id = new_bvs_id
            db.session.add(bnft)

        db.session.flush()

    def unavailable_benefit_handler(
        self,
        from_config_product_variation_id,
        to_config_product_variation_id,
    ):
        """
        This method handles the case where previously selected benefits are unavailable under the new product variation.
        """
        SB = Model_SelectionBenefit

        FROM = self._qry_benefit_mapper(
            from_config_product_variation_id, self.plan, self.t
        )
        TO = self._qry_benefit_mapper(to_config_product_variation_id, self.plan, self.t)

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
                SB.selection_plan_id == self.plan.selection_plan_id,
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
        if df_from.empty:
            raise RowNotFoundError("Cannot find existing product variation")

        df_to = pd.DataFrame(
            db.session.query(TO.c.config_product_variation_id).distinct().all()
        )
        if df_to.empty:
            raise RowNotFoundError("New product variation not found")

        df = pd.concat([df_from, df_to], ignore_index=True)

        if df.empty:
            raise ValidationError("No benefits found for the given product variations")
        if df["config_product_variation_id"].unique().size != 2:
            raise ValidationError("Invalid product variation selection")

    def update_product_variation(self, *args, **kwargs):
        validated_data = Schema_UpdateProductVariation().load(self.payload)

        from_config_product_variation_id = (
            self.plan.config_product_variation_state.config_product_variation_id
        )
        to_config_product_variation_id = validated_data["config_product_variation_id"]

        self.validate(
            from_config_product_variation_id, to_config_product_variation_id, self.plan
        )

        self.available_benefit_handler(
            from_config_product_variation_id,
            to_config_product_variation_id,
        )

        unavailable_benefits = self.unavailable_benefit_handler(
            from_config_product_variation_id, to_config_product_variation_id
        )

        new_product_variation_state = self.get_product_variation_state(
            to_config_product_variation_id
        )
        self.plan.config_product_variation_state_id = (
            new_product_variation_state.config_product_variation_state_id
        )
        db.session.add(self.plan)
        db.session.flush()

        benefit_schema = Schema_SelectionBenefit(many=True, exclude=("duration_sets",))
        return {
            **self.schema.dump(self.plan),
            "unavailable_benefits": benefit_schema.dump(unavailable_benefits),
        }
