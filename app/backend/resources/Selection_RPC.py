from flask import request
from flask_restx import Resource
from app.auth import authorization_required

from .Selection_RPC_PlanDesign import Selection_RPC_PlanDesign
from .Selection_RPC_Plan import Selection_RPC_Plan

SELECTION_EVENT_MAPPER = {
    # plan changes
    "create:plan-default": Selection_RPC_Plan.create_default_plan,
    "grant:plan": None,
    "revoke:plan": None,
    "update:plan": None,
    # mapper changes
    "update:rating_mapper": None,
    # plan design changes
    "update:product_plan_design": Selection_RPC_PlanDesign.update_product_plan_design,
    "update:coverage_plan_design": Selection_RPC_PlanDesign.update_coverage_plan_design,
    "remove:coverage_plan_design": None,
    # product variation changes
    "update:product_variation": None,
    # benefit changes
    "update:benefit": None,
    "remove:benefit": None,
    # benefit duration changes
    "update:benefit_duration": None,
    # age band changes
    "update:age_bands": None,
    # provision changes
    "update:provision": None,
}


class PayloadValidationError(Exception):
    pass


class Resource_Selection_RPC_Master(Resource):
    events = SELECTION_EVENT_MAPPER
    permissions = {"post": ["*"]}

    @classmethod
    @authorization_required
    def post(cls, event: str, *args, **kwargs):
        try:
            if event not in cls.events:
                raise PayloadValidationError("Invalid event")
            data = request.get_json()
            event_handler = cls.events[event]
            if event_handler is None:
                raise ValueError("Event handler not implemented")
            result = event_handler(
                payload=data, plan_id=kwargs.get("parent_id"), **kwargs
            )
            return {"status": "success", "data": result}, 200
        except PayloadValidationError as e:
            return {"status": "error", "msg": str(e)}, 400
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 500
