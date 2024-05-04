from marshmallow import Schema, fields, ValidationError
from app.extensions import db
from app.shared.errors import RowNotFoundError
from ..models import Model_SelectionAgeBand, Model_SelectionPlan
from ..schemas import Schema_SelectionAgeBand


class Schema_UpdateAgeBands(Schema):
    age_band_lower = fields.Integer(required=True)
    age_band_upper = fields.Integer(required=True)


class Selection_RPC_AgeBands:
    schema = Schema_SelectionAgeBand(many=True)

    def __init__(self, payload, plan_id, *args, **kwargs):
        self.payload = payload
        self.validated_data = Schema_UpdateAgeBands(many=True).load(payload)

        # this is additional validation that will throw an error if it fails
        self.validate(self.validated_data)

        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        if self.plan is None:
            raise RowNotFoundError("Plan not found")
        self.t = self.plan.plan_as_of_dts

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

    def update_age_bands(self, *args, **kwargs):
        db.session.query(Model_SelectionAgeBand).filter(
            Model_SelectionAgeBand.selection_plan_id == self.plan_id
        ).delete()
        age_bands = [
            Model_SelectionAgeBand(**age_band, selection_plan_id=self.plan_id)
            for age_band in self.validated_data
        ]
        db.session.add_all(age_bands)
        db.session.flush()
        return self.schema.dump(age_bands)
