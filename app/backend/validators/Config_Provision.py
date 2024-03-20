from typing import Union
from app.shared import BaseValidator, BaseListValidator
from app.shared.errors import AppValidationError
from ..models import Model_RefDataTypes, Model_ConfigDropdownSet, Model_ConfigProvision


class ValidatorMixin:
    @classmethod
    def validate_data_type_and_dropdown(
        cls, data_type_id: int, config_dropdown_set_id: Union[int, None]
    ):
        data_type = Model_RefDataTypes.find_one(data_type_id)
        if data_type is None:
            raise AppValidationError("Invalid data type")

        if data_type.ref_attr_code != "string":
            return
        dropdown_set = Model_ConfigDropdownSet.find_one(config_dropdown_set_id)
        if dropdown_set is None:
            raise AppValidationError(
                "A provision with data type `string` requires a dropdown list"
            )


class Validator_ConfigProvision(ValidatorMixin, BaseValidator):
    @classmethod
    def create(cls, payload, *args, **kwargs):
        data_type_id = payload.get("config_provision_data_type_id")
        config_dropdown_set_id = payload.get("config_dropdown_set_id")
        if data_type_id is None:
            raise AppValidationError("`config_provision_data_type_id` must be present")

        cls.validate_data_type_and_dropdown(data_type_id, config_dropdown_set_id)
        return payload

    @classmethod
    def replace(cls, payload, *args, **kwargs):
        data_type_id = payload.get("config_provision_data_type_id")
        config_dropdown_set_id = payload.get("config_dropdown_set_id")
        if data_type_id is None:
            raise AppValidationError("`config_provision_data_type_id` must be present")

        cls.validate_data_type_and_dropdown(data_type_id, config_dropdown_set_id)
        return payload

    @classmethod
    def update(cls, payload, *args, **kwargs):
        REQUIRED_KEYS = ["config_provision_data_type_id", "config_dropdown_set_id"]
        # if updating any fields in the REQUIRED KEYS, continu
        # otherwise, pass validation immediately
        if not any([k in REQUIRED_KEYS for k in payload.keys()]):
            return

        # if here, then at least one of the required keys is being updated
        # so we need to validate
        config_provision_id = payload["config_provision_id"]
        provision = Model_ConfigProvision.find_one(config_provision_id)
        data_type_id = payload.get(
            "config_provision_data_type_id", provision.config_provision_data_type_id
        )
        config_dropdown_set_id = payload.get(
            "config_dropdown_set_id", provision.config_dropdown_set_id
        )

        cls.validate_data_type_and_dropdown(data_type_id, config_dropdown_set_id)
        return payload


class Validator_ConfigProvisionList(ValidatorMixin, BaseListValidator):
    @classmethod
    def bulk_create(cls, payload, *args, **kwargs):
        for row in payload:
            data_type_id = row.get("config_provision_data_type_id")
            config_dropdown_set_id = row.get("config_dropdown_set_id")
            if data_type_id is None:
                raise AppValidationError(
                    "`config_provision_data_type_id` must be present"
                )

            cls.validate_data_type_and_dropdown(data_type_id, config_dropdown_set_id)
        return payload
