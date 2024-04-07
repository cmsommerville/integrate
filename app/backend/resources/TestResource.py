from logger import logger
from flask import request
from flask_restx import Resource
from sqlalchemy import event
from sqlalchemy.orm import Session
from app.extensions import db
from ..classes.TemporalSelectionQueries import (
    TemporalSelectionBenefits,
    Schema_TemporalSelectionBenefits_Plan,
)
from ..models import Model_SelectionPlan


@event.listens_for(Session, "do_orm_execute")
def receive_do_orm_execute(orm_execute_state):
    x = str(orm_execute_state.statement.compile(compile_kwargs={"literal_binds": True}))

    print("intercepted")


class TestResource(Resource):
    schema = Schema_TemporalSelectionBenefits_Plan()

    @classmethod
    def _get(cls, parent_id: int, *args, **kwargs):
        plan = TemporalSelectionBenefits.get_plan_asof_date(
            parent_id, t=request.args.get("t")
        )
        data = cls.schema.dump(plan)
        return data, 200

    @classmethod
    def get(cls, *args, **kwargs):
        qry = (
            db.session.query(Model_SelectionPlan)
            # .with_hint(
            #     Model_SelectionPlan, "FOR SYSTEM_TIME AS OF '2024-04-05 00:00:00'"
            # )
            .filter(Model_SelectionPlan.selection_plan_id == 3136)
            .first()
        )
        return {"hello": "world"}, 200
