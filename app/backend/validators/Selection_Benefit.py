from typing import Union
from app.shared import BaseValidator, BaseListValidator
from app.shared.errors import AppValidationError
from ..models import (
    Model_ConfigBenefitVariationState,
)


class ValidatorMixin:
    @classmethod
    def validate_benefit_amounts(
        cls, config_benefit_variation_state_id, selection_value, *args, **kwargs
    ):
        config_benefit_variation_state = Model_ConfigBenefitVariationState.find_one(
            config_benefit_variation_state_id
        )
        config_benefit = config_benefit_variation_state.benefit

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
    @classmethod
    def create(cls, payload, *args, **kwargs):
        cls.validate_benefit_amounts(**payload)

    @classmethod
    def replace(cls, payload, *args, **kwargs):
        cls.validate_benefit_amounts(**payload)

    @classmethod
    def update(cls, payload, *args, **kwargs):
        REQUIRED_KEYS = ["config_benefit_variation_state_id", "selection_value"]
        if not any([k in REQUIRED_KEYS for k in payload.keys()]):
            return
        cls.validate_benefit_amounts(**payload)


class Validator_SelectionBenefitList(ValidatorMixin, BaseListValidator):
    @classmethod
    def bulk_create(cls, payload, *args, **kwargs):
        _ = [cls.validate_benefit_amounts(**row) for row in payload]
