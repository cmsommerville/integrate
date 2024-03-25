from typing import List, Union
from marshmallow import Schema, fields
from app.extensions import db
from ..models import (
    Model_ConfigPlanDesignSet_Product,
    Model_ConfigPlanDesignSet_Coverage,
    Model_SelectionPlan,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
)
from ..schemas import Schema_SelectionBenefit


class Schema_UpdateProductPlanDesign(Schema):
    config_plan_design_set_id = fields.Integer(required=True)


class Schema_ExtractPlanDesignBenefits(Schema):
    config_benefit_variation_state_id = fields.Integer(required=True)
    selection_value = fields.Float(required=True)


class Selection_RPC_PlanDesign:
    schema_selection_benefit_list = Schema_SelectionBenefit(many=True)

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
        plan_design_benefits = []
        for coverage_plan_design in coverage_plan_designs:
            plan_design_benefits.extend(
                coverage_plan_design.get_plan_design_benefit_variation_states(
                    coverage_plan_design.config_plan_design_set_id,
                    plan.config_product_variation_state_id,
                )
            )
        return schema.dump(plan_design_benefits)

    @classmethod
    def merge_new_benefits(
        cls,
        parent: Union[Model_SelectionPlan, Model_SelectionCoverage],
        new_benefits_data: List[dict],
        coverage=None,
        *args,
        **kwargs,
    ):
        """
        This method adds, updates, and deletes benefits based on the new benefits from the selected plan design.
        """
        mapper = {
            benefit["config_benefit_variation_state_id"]: benefit["selection_value"]
            for benefit in new_benefits_data
        }

        old_plan_benefits = parent.benefits
        parent.benefits = []
        db.session.flush()

        new_plan_benefits_dict = {}
        for benefit in old_plan_benefits:
            # remove previously-selected benefits that are not in the plan design selection
            if benefit.config_benefit_variation_state_id not in mapper.keys():
                continue
            # update the selection value from the mapper
            benefit.selection_value = mapper[benefit.config_benefit_variation_state_id]
            new_plan_benefits_dict[benefit.config_benefit_variation_state_id] = benefit

        # add new benefits that are not in the old plan benefits
        for config_benefit_variation_state_id, selection_value in mapper.items():
            if config_benefit_variation_state_id in new_plan_benefits_dict.keys():
                continue
            new_plan_benefits_dict[config_benefit_variation_state_id] = (
                Model_SelectionBenefit(
                    selection_plan_id=parent.selection_plan_id,
                    selection_coverage_id=None,
                    config_benefit_variation_state_id=config_benefit_variation_state_id,
                    selection_value=selection_value,
                )
            )

        new_plan_benefits = list(new_plan_benefits_dict.values())
        parent.benefits = new_plan_benefits
        db.session.commit()
        return new_plan_benefits

    @classmethod
    def update_product_plan_design(cls, plan_id: int, data, *args, **kwargs):
        """
        Main callable for update:product_plan_design event.
        1. Fetches the product plan design and associated coverage plan designs.
        2. Extracts the plan design benefits by benefit-variation-state.
        3. Merges the new benefit variation state selections with previous selections (add/update/delete).
        """
        schema = Schema_UpdateProductPlanDesign()

        plan = cls.get_plan(plan_id)
        validated_data = schema.dump(data)
        product_plan_design = Model_ConfigPlanDesignSet_Product.find_one(
            validated_data["config_plan_design_set_id"]
        )

        if product_plan_design is None:
            raise Exception("Product plan design not found")

        plan_design_benefits = cls.extract_plan_design_benefits(
            product_plan_design.coverage_plan_designs, plan
        )
        selected_benefits = cls.merge_new_benefits(plan, plan_design_benefits)
        return cls.schema_selection_benefit_list.dump(selected_benefits)

    @classmethod
    def update_coverage_plan_design(cls, plan_id, data, *args, **kwargs):
        """
        Main callable for update:product_plan_design event.
        1. Fetches the product plan design and associated coverage plan designs.
        2. Extracts the plan design benefits by benefit-variation-state.
        3. Merges the new benefit variation state selections with previous selections (add/update/delete).
        """
        schema = Schema_UpdateProductPlanDesign()

        plan = cls.get_plan(plan_id)
        validated_data = schema.dump(data)
        coverage_plan_design = Model_ConfigPlanDesignSet_Coverage.find_one(
            validated_data["config_plan_design_set_id"]
        )

        if coverage_plan_design is None:
            raise Exception("Coverage plan design not found")

        plan_design_benefits = cls.extract_plan_design_benefits(
            [coverage_plan_design], plan
        )
        selected_benefits = cls.merge_new_benefits(
            plan,
            plan_design_benefits,
            coverage_id=coverage_plan_design.config_parent_id,
        )
        return cls.schema_selection_benefit_list.dump(selected_benefits)

    @classmethod
    def remove_coverage_plan_design(cls, plan_id, data, *args, **kwargs):
        pass
