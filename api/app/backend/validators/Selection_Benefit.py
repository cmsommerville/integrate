from app.extensions import db
from app.cache import cachedmethod
from app.shared import BaseValidator, BaseListValidator
from app.shared.errors import AppValidationError
from ..models import (
    Model_ConfigBenefitVariationState,
    Model_SelectionBenefit,
    Model_SelectionPlan,
)


class ValidatorMixin:
    @classmethod
    def get_selection_plan(cls, selection_plan_id: int):
        return Model_SelectionPlan.find_one(selection_plan_id)

    @classmethod
    def get_config_benefit_variation_state_id(cls, benefit_data):
        # this handles POST/PUT requests
        if benefit_data.get("config_benefit_variation_state_id") is not None:
            return benefit_data["config_benefit_variation_state_id"]
        # this handles PATCH requests
        elif benefit_data.get("selection_benefit_id") is not None:
            return Model_SelectionBenefit.find_one(
                benefit_data.get("selection_benefit_id")
            ).config_benefit_variation_state_id
        else:
            raise AppValidationError(
                "selection_benefit payload must contain the `config_benefit_variation_state_id` or the `selection_benefit_id`"
            )

    @classmethod
    def validate_benefit_amounts(
        cls,
        config_benefit_variation_state_id: int,
        selection_value: float,
        *args,
        **kwargs,
    ):
        config_benefit_variation_state = Model_ConfigBenefitVariationState.find_one(
            config_benefit_variation_state_id
        )
        config_benefit = config_benefit_variation_state.parent

        if not config_benefit:
            raise AppValidationError("Cannot find benefit")

        if float(config_benefit.min_value) > selection_value:
            raise AppValidationError(
                "Selection must be greater than minimum permissible value"
            )
        if float(config_benefit.max_value) < selection_value:
            raise AppValidationError(
                "Selection must be less than maximum permissible value"
            )
        if selection_value % float(config_benefit.step_value) != 0:
            raise AppValidationError(
                "Selection must be a multiple of the permissible step value"
            )


class Validator_SelectionBenefit(ValidatorMixin, BaseValidator):
    def __hash__(self):
        return hash(self.__class__)

    @classmethod
    def create(cls, payload, *args, **kwargs):
        config_plan_design_set_id = kwargs.get("config_plan_design_set_id")
        selection_plan_id = kwargs.get("plan_id")
        config_benefit_variation_state_id = cls.get_config_benefit_variation_state_id(
            payload
        )

        cls.validate_benefit_amounts(
            config_benefit_variation_state_id=config_benefit_variation_state_id,
            selection_value=payload["selection_value"],
        )
        return payload

    @classmethod
    def replace(cls, payload, *args, **kwargs):
        config_plan_design_set_id = kwargs.get("config_plan_design_set_id")
        selection_plan_id = kwargs.get("plan_id")
        config_benefit_variation_state_id = cls.get_config_benefit_variation_state_id(
            payload
        )
        cls.validate_benefit_amounts(
            config_benefit_variation_state_id=config_benefit_variation_state_id,
            selection_value=payload["selection_value"],
        )
        return payload

    @classmethod
    def update(cls, payload, *args, **kwargs):
        REQUIRED_KEYS = ["config_benefit_variation_state_id", "selection_value"]
        if not any([k in REQUIRED_KEYS for k in payload.keys()]):
            return

        config_plan_design_set_id = kwargs.get("config_plan_design_set_id")
        selection_plan_id = kwargs.get("plan_id")
        selection_benefit_id = kwargs.get("id")
        config_benefit_variation_state_id = cls.get_config_benefit_variation_state_id(
            {**payload, "selection_benefit_id": selection_benefit_id}
        )
        cls.validate_benefit_amounts(
            config_benefit_variation_state_id=config_benefit_variation_state_id,
            selection_value=payload["selection_value"],
        )
        return payload


class Validator_SelectionBenefitList(ValidatorMixin, BaseListValidator):
    @classmethod
    def bulk_create(cls, payload, *args, **kwargs):
        config_plan_design_set_id = kwargs.get("config_plan_design_set_id")
        selection_plan_id = kwargs.get("plan_id")
        _ = [
            cls.validate_benefit_amounts(
                config_benefit_variation_state_id=cls.get_config_benefit_variation_state_id(
                    row
                ),
                selection_value=row["selection_value"],
            )
            for row in payload
        ]
        return payload
