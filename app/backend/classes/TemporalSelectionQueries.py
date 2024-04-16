from itertools import groupby
from logger import logger
from app.extensions import db
from marshmallow import Schema, fields
from app.shared.utils import system_temporal_hint
from sqlalchemy.orm import attributes
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
    def load_plan(cls, selection_plan_id: int, t=None, *args, **kwargs):
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        return (
            db.session.query(PLAN)
            .filter(PLAN.selection_plan_id == selection_plan_id)
            .with_hint(PLAN, asof)
            .one()
        )

    @classmethod
    def load_benefits(cls, selection_plan_id: int, t=None, *args, **kwargs):
        pass

    @classmethod
    def load_coverages(cls, selection_plan_id: int, t=None, *args, **kwargs):
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        CVG = Model_SelectionCoverage
        BNFT = Model_SelectionBenefit
        DUR = Model_SelectionBenefitDuration
        objs = (
            db.session.query(CVG, BNFT, DUR)
            .select_from(PLAN)
            .join(CVG, PLAN.coverages)
            .join(BNFT, CVG.benefits)
            .join(DUR, BNFT.duration_sets, isouter=True)
            .filter(PLAN.selection_plan_id == selection_plan_id)
            .with_hint(PLAN, asof)
            .with_hint(CVG, asof)
            .with_hint(BNFT, asof)
            .with_hint(DUR, asof)
            .all()
        )

        coverages = sorted(
            list(set([cvg for cvg, _, _ in objs])),
            key=lambda obj: obj.selection_coverage_id,
        )
        benefits = sorted(
            list(set([bnft for _, bnft, _ in objs])),
            key=lambda obj: obj.selection_coverage_id,
        )
        duration_sets = sorted(
            list(set([dur for _, _, dur in objs if dur is not None])),
            key=lambda obj: obj.selection_benefit_id,
        )
        duration_sets = dict(
            (k, list(v))
            for k, v in groupby(
                duration_sets,
                key=lambda obj: obj.selection_benefit_id,
            )
        )
        for benefit in benefits:
            attributes.set_committed_value(
                benefit,
                "duration_sets",
                duration_sets.get(benefit.selection_benefit_id, []),
            )

        benefits = dict(
            (k, list(v))
            for k, v in groupby(
                benefits,
                key=lambda obj: obj.selection_coverage_id,
            )
        )
        for coverage in coverages:
            attributes.set_committed_value(
                coverage,
                "benefits",
                benefits.get(coverage.selection_coverage_id, []),
            )

        return coverages

    @classmethod
    def load_provisions(cls, selection_plan_id: int, t=None, *args, **kwargs):
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        PROV = Model_SelectionProvision
        return (
            db.session.query(PROV)
            .select_from(PLAN)
            .join(PROV, PROV.selection_plan_id == PLAN.selection_plan_id)
            .filter(PLAN.selection_plan_id == selection_plan_id)
            .with_hint(PLAN, asof)
            .with_hint(PROV, asof)
            .all()
        )

    @classmethod
    def load_rating_mappers(cls, selection_plan_id: int, t=None, *args, **kwargs):
        asof = system_temporal_hint(t)
        PLAN = Model_SelectionPlan
        RMS = Model_SelectionRatingMapperSet
        return (
            db.session.query(RMS)
            .select_from(PLAN)
            .join(RMS, RMS.selection_plan_id == PLAN.selection_plan_id)
            .filter(PLAN.selection_plan_id == selection_plan_id)
            .with_hint(RMS, asof)
            .with_hint(RMS, asof)
            .all()
        )

    @classmethod
    def get_plan_asof_date(cls, selection_plan_id: int, t=None, *args, **kwargs):
        """
        Fetch plan + coverages + benefits + duration_sets for a given `selection_plan_id` as of time `t`.
        If no time is provided, fetch the latest data.
        """
        plan = cls.load_plan(selection_plan_id, t)
        provisions = cls.load_provisions(selection_plan_id, t)
        coverages = cls.load_coverages(selection_plan_id, t)
        rating_mappers = cls.load_rating_mappers(selection_plan_id, t)

        attributes.set_committed_value(plan, "provisions", provisions)
        attributes.set_committed_value(plan, "coverages", coverages)
        attributes.set_committed_value(plan, "rating_mapper_sets", rating_mappers)

        return plan
