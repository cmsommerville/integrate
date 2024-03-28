from app.extensions import db
from marshmallow import Schema, fields
from app.shared.utils import system_temporal_hint
from sqlalchemy.orm import joinedload
from ..models import (
    Model_SelectionBenefit,
    Model_SelectionBenefitDuration,
    Model_SelectionCoverage,
    Model_SelectionPlan,
    Model_SelectionProvision,
    Model_SelectionFactor,
)


class Schema_TemporalSelectionBenefits_BenefitDuration(Schema):
    selection_benefit_duration_id = fields.Integer()
    selection_benefit_id = fields.Integer()
    config_benefit_duration_set_id = fields.Integer()
    config_benefit_duration_detail_id = fields.Integer()
    selection_factor = fields.Float()


class Schema_TemporalSelectionBenefits_Benefit(Schema):
    selection_benefit_id = fields.Integer()
    selection_plan_id = fields.Integer()
    selection_coverage_id = fields.Integer()
    config_benefit_variation_state_id = fields.Integer()
    selection_value = fields.Float()
    duration_sets = fields.Nested(
        Schema_TemporalSelectionBenefits_BenefitDuration, many=True
    )


class Schema_TemporalSelectionBenefits_Coverage(Schema):
    selection_coverage_id = fields.Integer()
    selection_plan_id = fields.Integer()
    config_coverage_id = fields.Integer()
    config_plan_design_set_id = fields.Integer()
    benefits = fields.Nested(Schema_TemporalSelectionBenefits_Benefit, many=True)


class Schema_TemporalSelectionBenefits_Factor(Schema):
    selection_factor_id = fields.Integer()
    selection_provision_id = fields.Integer()
    config_factor_set_id = fields.Integer()
    config_factor_id = fields.Integer()
    selection_rate_table_age_value = fields.Integer()
    selection_rating_attr_id1 = fields.Integer()
    selection_rating_attr_id2 = fields.Integer()
    selection_rating_attr_id3 = fields.Integer()
    selection_rating_attr_id4 = fields.Integer()
    selection_rating_attr_id5 = fields.Integer()
    selection_rating_attr_id6 = fields.Integer()
    selection_factor_value = fields.Float()


class Schema_TemporalSelectionBenefits_Provision(Schema):
    selection_provision_id = fields.Integer()
    selection_plan_id = fields.Integer()
    config_provision_state_id = fields.Integer()
    selection_value = fields.String()
    factors = fields.Nested(Schema_TemporalSelectionBenefits_Factor, many=True)


class Schema_TemporalSelectionBenefits_SitusState(Schema):
    state_id = fields.Integer()
    state_code = fields.String()
    state_name = fields.String()


class Schema_TemporalSelectionBenefits_Plan(Schema):
    selection_plan_id = fields.Integer()
    config_product_id = fields.Integer()
    selection_plan_effective_date = fields.Date()
    situs_state_id = fields.Integer()
    config_product_variation_state_id = fields.Integer()
    selection_group_id = fields.Integer()
    cloned_from_selection_plan_id = fields.Integer()
    is_template = fields.Boolean()
    plan_status = fields.Integer()

    situs_state = fields.Nested(Schema_TemporalSelectionBenefits_SitusState)
    coverages = fields.Nested(Schema_TemporalSelectionBenefits_Coverage, many=True)
    provisions = fields.Nested(Schema_TemporalSelectionBenefits_Provision, many=True)


class TemporalSelectionBenefits:
    @classmethod
    def load_plan_asof_date(cls, selection_plan_id: int, t=None, *args, **kwargs):
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        CVG = Model_SelectionCoverage
        BNFT = Model_SelectionBenefit
        DUR = Model_SelectionBenefitDuration
        PROV = Model_SelectionProvision
        FCTR = Model_SelectionFactor
        qry = (
            db.session.query(PLAN, CVG, BNFT, DUR, PROV, FCTR)
            .select_from(BNFT)
            .join(DUR, BNFT.duration_sets, isouter=True)
            .join(CVG, BNFT.selection_coverage_id == CVG.selection_coverage_id)
            .join(PLAN, BNFT.selection_plan_id == PLAN.selection_plan_id)
            .join(PROV, PROV.selection_plan_id == PLAN.selection_plan_id)
            .join(
                FCTR,
                FCTR.selection_provision_id == PROV.selection_provision_id,
            )
            .with_hint(PLAN, asof)
            .with_hint(CVG, asof)
            .with_hint(BNFT, asof)
            .with_hint(DUR, asof)
            .with_hint(PROV, asof)
            .with_hint(FCTR, asof)
            .filter(BNFT.selection_plan_id == selection_plan_id)
        )
        results = qry.all()
        return results

    @classmethod
    def get_plan_asof_date(cls, selection_plan_id: int, t=None, *args, **kwargs):
        """
        Fetch plan + coverages + benefits + duration_sets for a given `selection_plan_id` as of time `t`.
        If no time is provided, fetch the latest data.
        """
        # this method just loads the data into SQLAlchemy's identity map
        res = cls.load_plan_asof_date(selection_plan_id, t, *args, **kwargs)

        # requery the plan to pull data from the identity map
        # it is very tricky to setup this query to prevent marshmallow from refetching data on serialization
        # CRITICAL: query should not refetch from database
        qry = (
            db.session.query(Model_SelectionPlan)
            .filter_by(selection_plan_id=selection_plan_id)
            .options(
                joinedload(Model_SelectionPlan.coverages)
                .joinedload(Model_SelectionCoverage.benefits)
                .joinedload(Model_SelectionBenefit.duration_sets, innerjoin=False),
                joinedload(Model_SelectionPlan.situs_state),
                joinedload(Model_SelectionPlan.provisions).joinedload(
                    Model_SelectionProvision.factors
                ),
            )
        )
        plan = qry.one()
        db.session.expunge(plan)
        return plan
