from typing import List, Union
from marshmallow import Schema, fields
from sqlalchemy.orm import joinedload
from app.extensions import db
from ..models import (
    Model_ConfigPlanDesignSet_Product,
    Model_ConfigPlanDesignSet_Coverage,
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationSet,
    Model_ConfigBenefitDurationDetailAuth_ACL,
    Model_ConfigBenefit,
    Model_ConfigBenefitVariationState,
    Model_SelectionPlan,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
    Model_SelectionBenefitDuration,
)
from ..schemas import Schema_SelectionCoverage


class Schema_UpdateProductPlanDesign(Schema):
    config_plan_design_set_id = fields.Integer(required=True)


class Schema_UpdateCoveragePlanDesign(Schema):
    config_plan_design_set_id = fields.Integer(required=True)


class Schema_RemoveCoveragePlanDesign(Schema):
    selection_coverage_id = fields.Integer(required=True)


class Schema_ExtractPlanDesignBenefits(Schema):
    config_benefit_variation_state_id = fields.Integer(required=True)
    selection_value = fields.Float(required=True)


class Selection_RPC_PlanDesign:
    schema_selection_benefit_list = Schema_SelectionCoverage(many=True)

    @classmethod
    def get_plan(cls, plan_id):
        return Model_SelectionPlan.find_one(plan_id)

    @classmethod
    def extract_plan_design_benefits(
        cls,
        coverage_plan_designs: List[Model_ConfigPlanDesignSet_Coverage],
        plan: Model_SelectionPlan,
        *args,
        **kwargs,
    ):
        schema = Schema_ExtractPlanDesignBenefits(many=True)
        coverages = []
        for coverage_plan_design in coverage_plan_designs:
            coverage = {
                "config_coverage_id": coverage_plan_design.config_parent_id,
                "benefits": [],
            }
            coverage["benefits"].extend(
                schema.dump(
                    coverage_plan_design.get_plan_design_benefit_variation_states(
                        coverage_plan_design.config_plan_design_set_id,
                        plan.config_product_variation_state_id,
                    )
                )
            )
            coverages.append(coverage)
        return coverages

    @classmethod
    def merge_new_benefits_by_coverage(
        cls,
        plan: Model_SelectionPlan,
        new_benefits_data: List[dict],
        config_coverage_id: int,
        *args,
        **kwargs,
    ):
        """
        This method adds, updates, and deletes benefits based on the new benefits from the selected plan design.
        """
        # a mapper of BVS to plan design selection value
        mapper = {
            benefit["config_benefit_variation_state_id"]: benefit["selection_value"]
            for benefit in new_benefits_data
        }

        # get the selection coverage, if it exists
        selection_coverage = (
            db.session.query(Model_SelectionCoverage)
            .options(joinedload(Model_SelectionCoverage.benefits))
            .filter(
                Model_SelectionCoverage.config_coverage_id == config_coverage_id,
                Model_SelectionCoverage.selection_plan_id == plan.selection_plan_id,
            )
            .one_or_none()
        )

        # if it doesn't exist, create it
        if selection_coverage is None:
            selection_coverage = Model_SelectionCoverage(
                selection_plan_id=plan.selection_plan_id,
                config_coverage_id=config_coverage_id,
            )
            db.session.add(selection_coverage)
            db.session.flush()

        ########## NOW THE SELECTION COVERAGE EXISTS ##########

        # clear the existing selection benefits
        old_cvg_benefits = selection_coverage.benefits
        selection_coverage.benefits = []
        db.session.flush()

        new_cvg_benefits_dict = {}
        for benefit in old_cvg_benefits:
            # remove previously-selected benefits that are not in the plan design selection
            if benefit.config_benefit_variation_state_id not in mapper.keys():
                continue
            # update the selection value from the mapper
            benefit.selection_value = mapper[benefit.config_benefit_variation_state_id]
            new_cvg_benefits_dict[benefit.config_benefit_variation_state_id] = benefit

        # add new benefits that are not in the old plan benefits
        for config_benefit_variation_state_id, selection_value in mapper.items():
            if config_benefit_variation_state_id in new_cvg_benefits_dict.keys():
                continue
            new_cvg_benefits_dict[config_benefit_variation_state_id] = (
                Model_SelectionBenefit(
                    selection_plan_id=plan.selection_plan_id,
                    selection_coverage_id=selection_coverage.selection_coverage_id,
                    config_benefit_variation_state_id=config_benefit_variation_state_id,
                    selection_value=selection_value,
                )
            )

        new_cvg_benefits = list(new_cvg_benefits_dict.values())
        selection_coverage.benefits = new_cvg_benefits
        db.session.flush()
        cls.merge_new_benefit_durations(selection_coverage.benefits, plan)
        return selection_coverage

    @classmethod
    def merge_new_benefit_durations(
        cls, selection_benefits: List[Model_SelectionBenefit], plan: Model_SelectionPlan
    ):
        """
        For each benefit in the selection_benefits list, this method adds the benefit duration details that are not already selected.
        It does not reset existing benefit duration selections to the default values.
        If a required benefit duration is not selected, it will create a record and set to the default.
        """
        selection_mapper = {
            benefit.config_benefit_variation_state_id: benefit
            for benefit in selection_benefits
        }
        BVS = Model_ConfigBenefitVariationState
        BNFT = Model_ConfigBenefit
        BDD = Model_ConfigBenefitDurationDetail
        BDDACL = Model_ConfigBenefitDurationDetailAuth_ACL
        BDS = Model_ConfigBenefitDurationSet
        SBD = Model_SelectionBenefitDuration
        SB = Model_SelectionBenefit

        # get the existing selected benefit durations
        existing_benefit_durations = (
            db.session.query(
                SB.config_benefit_variation_state_id, SBD.selection_benefit_duration_id
            )
            .join(SB, SB.selection_benefit_id == SBD.selection_benefit_id)
            .filter(
                SB.selection_plan_id == plan.selection_plan_id,
                SB.config_benefit_variation_state_id.in_(selection_mapper.keys()),
            )
            .subquery()
        )

        # this query is all the required benefit duration sets that are not selected yet
        rows = (
            db.session.query(
                BVS.config_benefit_variation_state_id,
                BDD.config_benefit_duration_detail_id,
                BDD.config_benefit_duration_set_id,
                BDD.config_benefit_duration_factor,
            )
            .select_from(BDD)
            .join(
                BDDACL,
                BDDACL.config_benefit_duration_detail_id
                == BDD.config_benefit_duration_detail_id,
            )
            .join(
                BDS,
                BDS.config_benefit_duration_set_id
                == BDD.config_benefit_duration_set_id,
            )
            .join(BNFT, BNFT.config_benefit_id == BDS.config_benefit_id)
            .join(BVS, BVS.config_benefit_id == BNFT.config_benefit_id)
            .join(
                existing_benefit_durations,
                existing_benefit_durations.c.config_benefit_variation_state_id
                == BVS.config_benefit_variation_state_id,
                isouter=True,
            )
            .filter(
                BVS.config_benefit_variation_state_id.in_(selection_mapper.keys()),
                existing_benefit_durations.c.selection_benefit_duration_id == None,
            )
            .distinct()
            .all()
        )

        # these are required, but unselected, benefit durations
        # loop over and create the duration records
        for row in rows:
            bvs, bdd, bds, factor = row
            selection_benefit = selection_mapper.get(
                row.config_benefit_variation_state_id
            )
            if selection_benefit is None:
                continue
            selection_benefit_duration = Model_SelectionBenefitDuration(
                selection_benefit_id=selection_benefit.selection_benefit_id,
                config_benefit_duration_detail_id=bdd,
                config_benefit_duration_set_id=bds,
                selection_factor=float(factor),
            )
            db.session.add(selection_benefit_duration)
        db.session.flush()

    @classmethod
    def update_product_plan_design(cls, payload, plan_id: int, *args, **kwargs):
        """
        Main callable for upsert:product_plan_design event.
        1. Fetches the product plan design and associated coverage plan designs.
        2. Extracts the plan design benefits by benefit-variation-state.
        3. Merges the new benefit variation state selections with previous selections (add/update/delete).
        """
        schema = Schema_UpdateProductPlanDesign()

        plan = cls.get_plan(plan_id)
        validated_data = schema.dump(payload)
        product_plan_design = Model_ConfigPlanDesignSet_Product.find_one(
            validated_data["config_plan_design_set_id"]
        )

        if product_plan_design is None:
            raise Exception("Product plan design not found")

        plan_design_benefits = cls.extract_plan_design_benefits(
            product_plan_design.coverage_plan_designs, plan
        )
        coverages = []
        for cvg in plan_design_benefits:
            coverages.append(
                cls.merge_new_benefits_by_coverage(
                    plan, cvg["benefits"], cvg["config_coverage_id"]
                )
            )
        return cls.schema_selection_benefit_list.dump(coverages)

    @classmethod
    def upsert_coverage_plan_design(cls, payload, plan_id, *args, **kwargs):
        """
        Main callable for update:coverage_plan_design event.
        1. Fetches the coverage plan design.
        2. Extracts the plan design benefits by benefit-variation-state.
        3. Merges the new benefit variation state selections with previous selections (add/update/delete).
        """
        schema = Schema_UpdateCoveragePlanDesign()

        plan = cls.get_plan(plan_id)
        validated_data = schema.dump(payload)
        coverage_plan_design = Model_ConfigPlanDesignSet_Coverage.find_one_by_attr(
            validated_data
        )

        if coverage_plan_design is None:
            raise Exception("Coverage plan design not found")

        plan_design_benefits = cls.extract_plan_design_benefits(
            [coverage_plan_design], plan
        )[0]
        selected_benefits = cls.merge_new_benefits_by_coverage(
            plan,
            plan_design_benefits["benefits"],
            config_coverage_id=coverage_plan_design.config_parent_id,
        )
        return cls.schema_selection_benefit_list.dump(selected_benefits, many=False)

    @classmethod
    def remove_coverage_plan_design(cls, payload, plan_id, *args, **kwargs):
        """
        Main callable for remove:coverage_plan_design event.
        1. Fetches the coverage.
        2. Sets the benefits relationship to an empty list and flushes
        """
        schema = Schema_RemoveCoveragePlanDesign()

        validated_data = schema.dump(payload)
        coverage = Model_SelectionCoverage.find_one_by_attr(
            {**validated_data, "selection_plan_id": plan_id}
        )

        if coverage is None:
            raise Exception("Coverage plan design not found")

        coverage.benefits = []
        db.session.flush()
        return cls.schema_selection_benefit_list.dump(coverage, many=False)
