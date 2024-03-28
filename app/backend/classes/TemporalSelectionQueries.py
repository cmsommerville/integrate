from logger import logger
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
    Model_SelectionRatingMapperSet,
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


class Schema_TemporalSelectionBenefits_RatingMapperSet(Schema):
    selection_rating_mapper_set_id = fields.Integer()
    selection_plan_id = fields.Integer()
    selection_rating_mapper_set_type = fields.String()
    config_rating_mapper_set_id = fields.Integer()
    has_custom_weights = fields.Boolean()


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
    rating_mapper_sets = fields.Nested(
        Schema_TemporalSelectionBenefits_RatingMapperSet, many=True
    )


class TemporalSelectionBenefits:
    @classmethod
    def load_plan_asof_date(cls, selection_plan_id: int, t=None, *args, **kwargs):
        """
        This is a tricky method!

        The first query loads the relevant selection instances as of the correct point in time into the identity map.
        The format of the output is difficult because it is a list of tuples.

        The second query pulls the plan instance plus all relevant collections. This query must be designed
        to eagerly pull from the identity map, which is why the first query is necessary.
        """
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        CVG = Model_SelectionCoverage
        BNFT = Model_SelectionBenefit
        DUR = Model_SelectionBenefitDuration
        PROV = Model_SelectionProvision
        FCTR = Model_SelectionFactor
        RMS = Model_SelectionRatingMapperSet
        qry = (
            db.session.query(PLAN, CVG, BNFT, DUR, PROV, FCTR, RMS)
            .select_from(PLAN)
            .join(CVG, PLAN.coverages, isouter=True)
            .join(PROV, PLAN.provisions, isouter=True)
            .join(BNFT, CVG.benefits, isouter=True)
            .join(DUR, BNFT.duration_sets, isouter=True)
            .join(FCTR, PROV.factors, isouter=True)
            .join(RMS, PLAN.rating_mapper_sets, isouter=True)
            .filter(PLAN.selection_plan_id == selection_plan_id)
            .with_hint(PLAN, asof)
            .with_hint(CVG, asof)
            .with_hint(BNFT, asof)
            .with_hint(DUR, asof)
            .with_hint(PROV, asof)
            .with_hint(FCTR, asof)
            .with_hint(RMS, asof)
        )
        _ = qry.all()

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
                joinedload(Model_SelectionPlan.rating_mapper_sets),
            )
        )
        plan = qry.one()
        return plan

    @classmethod
    def get_plan_asof_date(cls, selection_plan_id: int, t=None, *args, **kwargs):
        """
        Fetch plan + coverages + benefits + duration_sets for a given `selection_plan_id` as of time `t`.
        If no time is provided, fetch the latest data.
        """
        return cls.load_plan_asof_date(selection_plan_id, t, *args, **kwargs)
