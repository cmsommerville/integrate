from marshmallow import Schema, fields, validates_schema, ValidationError
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError
from ..models import (
    Model_ConfigBenefit,
    Model_ConfigBenefitVariationState,
    Model_SelectionCoverage,
    Model_SelectionBenefit,
)
from ..schemas import (
    Schema_SelectionBenefit,
)


class RowNotFoundError(Exception):
    pass


class Schema_UpdateBenefitDuration(Schema):
    selection_benefit_id = fields.Integer(required=False)
    config_benefit_variation_state_id = fields.Integer(required=False)
    selection_value = fields.Float(required=True)
    version_id = fields.String(required=False)

    @validates_schema
    def validate_update_or_insert(self, data, **kwargs):
        """
        Validate that if the rate groups assigned to each benefit are defined on the product
        """
        if (data.get("selection_benefit_id") is not None) and (
            data.get("version_id") is not None
        ):
            pass
        elif data.get("config_benefit_variation_state_id") is not None:
            pass
        else:
            raise ValidationError(
                "Either selection_benefit_id + version_id or config_benefit_variation_state_id must be provided"
            )


class Schema_RemoveBenefit(Schema):
    selection_benefit_id = fields.Integer(required=True)
    version_id = fields.String(required=True)


class Selection_RPC_BenefitDuration:
    schema = Schema_SelectionBenefit()

    @classmethod
    def update_benefit_duration(cls, payload, plan_id, *args, **kwargs):
        """
        Update the existing selection benefit duration.
        """
        pass
