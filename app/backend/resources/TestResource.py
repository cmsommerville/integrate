from flask import request
from flask_restx import Resource
from ..classes.TemporalSelectionQueries import (
    TemporalSelectionBenefits,
    Schema_TemporalSelectionBenefits_Plan,
)


class TestResource(Resource):
    schema = Schema_TemporalSelectionBenefits_Plan()

    @classmethod
    def get(cls, parent_id: int, *args, **kwargs):
        plan = TemporalSelectionBenefits.get_plan_asof_date(
            parent_id, t=request.args.get("t")
        )
        data = cls.schema.dump(plan)
        return data, 200
