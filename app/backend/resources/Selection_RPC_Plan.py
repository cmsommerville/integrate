from marshmallow import Schema, fields
from app.extensions import db
from app.auth import get_user
from ..models import (
    Model_ConfigPlanDesignDetail_Benefit,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitVariationState,
    Model_DefaultProductRatingMapperSet,
    Model_SelectionAgeBand,
    Model_SelectionPlan,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
    Model_SelectionBenefitDuration,
)
from ..schemas import (
    Schema_SelectionPlan,
    Schema_DefaultProductRatingMapperSet_For_Selection,
    Schema_SelectionRatingMapperSet,
)

WITH_GRANT_OPTION = True


class Schema_UpdateProductPlanDesign(Schema):
    config_plan_design_set_id = fields.Integer(required=True)


class Schema_ExtractPlanDesignBenefits(Schema):
    config_benefit_variation_state_id = fields.Integer(required=True)
    selection_value = fields.Float(required=True)


class Selection_RPC_Plan:
    schema = Schema_SelectionPlan()

    @classmethod
    def _qry_plan_design_benefits(
        cls, config_plan_design_set_id: int, product_variation_state_id: int
    ):
        PDB = Model_ConfigPlanDesignDetail_Benefit
        BVS = Model_ConfigBenefitVariationState
        BD = Model_ConfigBenefitDurationSet
        BDD = Model_ConfigBenefitDurationDetail
        qry = (
            db.session.query(
                BVS.config_benefit_variation_state_id,
                PDB.default_value,
                BD.config_benefit_duration_set_id,
                BD.default_config_benefit_duration_detail_id,
                BDD.config_benefit_duration_factor,
            )
            .select_from(PDB)
            .join(BVS, BVS.config_benefit_id == PDB.config_parent_id)
            .join(BD, BD.config_benefit_id == BVS.config_benefit_id, isouter=True)
            .join(
                BDD,
                BD.default_config_benefit_duration_detail_id
                == BDD.config_benefit_duration_detail_id,
                isouter=True,
            )
            .filter(
                PDB.config_plan_design_set_id == config_plan_design_set_id,
                BVS.config_product_variation_state_id == product_variation_state_id,
            )
        )
        return qry.all()

    @classmethod
    def load_plan_design_to_selection_benefit(
        cls,
        config_plan_design_set_id: int,
        product_variation_state_id: int,
        selection_plan_id: int,
    ):
        """
        Set a plan's benefits (which are by benefit variation state ID)
        based on a plan design selection (which are by benefit ID).
        """
        rows = cls._qry_plan_design_benefits(
            config_plan_design_set_id, product_variation_state_id
        )
        objs_dict = {}
        for row in rows:
            (
                config_benefit_variation_state_id,
                default_benefit_value,
                config_benefit_duration_set_id,
                default_config_benefit_duration_detail_id,
                config_benefit_duration_factor,
            ) = row
            bnft_key = (
                selection_plan_id,
                config_benefit_variation_state_id,
                float(default_benefit_value),
            )
            if bnft_key not in objs_dict:
                objs_dict[bnft_key] = Model_SelectionBenefit(
                    selection_plan_id=selection_plan_id,
                    config_benefit_variation_state_id=config_benefit_variation_state_id,
                    selection_value=float(default_benefit_value),
                )

            if config_benefit_duration_set_id is not None:
                objs_dict[bnft_key].duration_sets.append(
                    Model_SelectionBenefitDuration(
                        **{
                            "config_benefit_duration_set_id": config_benefit_duration_set_id,
                            "config_benefit_duration_detail_id": default_config_benefit_duration_detail_id,
                            "selection_factor": float(config_benefit_duration_factor),
                        }
                    )
                )
        return list(objs_dict.values())

    @classmethod
    def create_default_coverage_benefits(
        cls, plan: Model_SelectionPlan, *args, **kwargs
    ):
        default_product_plan_design = (
            plan.config_product_variation_state.default_product_plan_design
        )
        default_coverage_plan_designs = (
            default_product_plan_design.coverage_plan_designs
        )
        selection_coverages = []
        for cpd in default_coverage_plan_designs:
            coverage = Model_SelectionCoverage(
                selection_plan_id=plan.selection_plan_id,
                config_coverage_id=cpd.config_parent_id,
                config_plan_design_set_id=cpd.config_plan_design_set_id,
            )
            coverage.benefits = cls.load_plan_design_to_selection_benefit(
                cpd.config_plan_design_set_id,
                plan.config_product_variation_state_id,
                plan.selection_plan_id,
            )
            selection_coverages.append(coverage)
        return selection_coverages

    @classmethod
    def create_default_age_bands(cls, plan: Model_SelectionPlan, *args, **kwargs):
        default_age_band_set = plan.config_product_variation_state.age_band_set
        if default_age_band_set is None:
            return Model_SelectionAgeBand(
                selection_plan_id=plan.selection_plan_id,
                age_band_lower=0,
                age_band_upper=999,
            )

        return [
            Model_SelectionAgeBand(
                selection_plan_id=plan.selection_plan_id,
                age_band_lower=ab.age_band_lower,
                age_band_upper=ab.age_band_upper,
            )
            for ab in default_age_band_set.age_bands
        ]

    @classmethod
    def create_default_rating_mappers(cls, plan: Model_SelectionPlan, *args, **kwargs):
        schema = Schema_DefaultProductRatingMapperSet_For_Selection(many=True)
        selection_schema = Schema_SelectionRatingMapperSet(many=True)
        objs = Model_DefaultProductRatingMapperSet.find_by_parent(
            plan.config_product_id
        )
        data = schema.dump(objs)
        return selection_schema.load(
            [{**row, "selection_plan_id": plan.selection_plan_id} for row in data]
        )

    @classmethod
    def create_plan_acl(cls):
        user = get_user()
        return {
            "user_name": user.get("user_name"),
            "with_grant_option": WITH_GRANT_OPTION,
        }

    @classmethod
    def create_default_plan(cls, payload, *args, **kwargs):
        try:
            plan = cls.schema.load({**payload, "acl": [cls.create_plan_acl()]})
            db.session.add(plan)
            db.session.flush()

            selection_rating_mappers = cls.create_default_rating_mappers(plan)
            db.session.add_all(selection_rating_mappers)

            selection_age_bands = cls.create_default_age_bands(plan)
            db.session.add_all(selection_age_bands)

            selection_coverage_benefits = cls.create_default_coverage_benefits(plan)
            db.session.add_all(selection_coverage_benefits)
            db.session.commit()
            return cls.schema.dump(plan)
        except Exception as e:
            db.session.rollback()
            raise e
