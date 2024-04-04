from marshmallow import Schema, fields, ValidationError
from app.extensions import db
from ..models import Model_SelectionAgeBand
from ..schemas import Schema_SelectionAgeBand


class RowNotFoundError(Exception):
    pass


class Schema_UpdateAgeBands(Schema):
    age_band_lower = fields.Integer(required=True)
    age_band_upper = fields.Integer(required=True)


class Selection_RPC_AgeBands:
    schema = Schema_SelectionAgeBand(many=True)

    @classmethod
    def validate(cls, payload, *args, **kwargs):
        age_bands = sorted(payload, key=lambda x: x["age_band_lower"])
        if len(age_bands) == 0:
            raise ValidationError("Age bands are required")
        for i, age_band in enumerate(age_bands):
            if age_band["age_band_lower"] < 0:
                raise ValidationError("Age band lower bounds must be non-negative")
            if age_band["age_band_upper"] < age_band["age_band_lower"]:
                raise ValidationError(
                    "Age band upper bounds must be greater than or equal to lower bounds"
                )
            if (
                i > 0
                and age_band["age_band_lower"] != age_bands[i - 1]["age_band_upper"] + 1
            ):
                raise ValidationError(
                    "Lower age band must be one greater than the previous upper age band"
                )

    @classmethod
    def update_age_bands(cls, payload, plan_id, *args, **kwargs):
        validated_data = Schema_UpdateAgeBands(many=True).load(payload)
        cls.validate(validated_data)

        db.session.query(Model_SelectionAgeBand).filter(
            Model_SelectionAgeBand.selection_plan_id == plan_id
        ).delete()
        age_bands = [
            Model_SelectionAgeBand(**age_band, selection_plan_id=plan_id)
            for age_band in validated_data
        ]
        db.session.add_all(age_bands)
        db.session.flush()
