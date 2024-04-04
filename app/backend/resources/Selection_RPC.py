from flask import request
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from app.auth import authorization_required, NotAuthorizedError
from app.shared.errors import PlanInvalidError
from app.extensions import db

from .Selection_RPC_AgeBands import Selection_RPC_AgeBands
from .Selection_RPC_Benefit import Selection_RPC_Benefit
from .Selection_RPC_BenefitDuration import Selection_RPC_BenefitDuration
from .Selection_RPC_PlanDesign import Selection_RPC_PlanDesign
from .Selection_RPC_Plan import Selection_RPC_Plan
from .Selection_RPC_Provision import Selection_RPC_Provision
from .Selection_RPC_RatingMapper import Selection_RPC_RatingMapper
from ..schemas import Schema_EventLog


# Do not commit/rollback in the event handlers; just flush results
SELECTION_EVENT_MAPPER = {
    # plan changes
    "create:plan-default": Selection_RPC_Plan.create_default_plan,
    "grant:plan": Selection_RPC_Plan.grant_plan,
    "revoke:plan": Selection_RPC_Plan.revoke_plan,
    "update:plan": None,
    # mapper changes
    "update:rating_mapper": Selection_RPC_RatingMapper.update_rating_mapper,
    # plan design changes
    "update:product_plan_design": Selection_RPC_PlanDesign.update_product_plan_design,
    "update:coverage_plan_design": Selection_RPC_PlanDesign.update_coverage_plan_design,
    "remove:coverage_plan_design": None,
    # product variation changes
    "update:product_variation": None,  # this is tricky because we need to port the benefits to different BVS's
    # benefit changes
    "upsert:benefit": Selection_RPC_Benefit.upsert_benefit,  # this should update or create a benefit; should not require client to differentiate
    "remove:benefit": Selection_RPC_Benefit.remove_benefit,
    # benefit duration changes
    "update:benefit_duration": Selection_RPC_BenefitDuration.update_benefit_duration,
    # age band changes
    "update:age_bands": Selection_RPC_AgeBands.update_age_bands,
    # provision changes
    "update:provision": Selection_RPC_Provision.update_provision,
}


class PayloadValidationError(Exception):
    pass


class Resource_Selection_RPC_Dispatcher(Resource):
    events = SELECTION_EVENT_MAPPER
    permissions = {"post": ["write:selection"]}
    event_log_schema = Schema_EventLog()

    @classmethod
    def log_event(cls, event: str, payload: dict, **kwargs):
        event_log = cls.event_log_schema.load(
            {
                "event_type_code": event,
                "event_payload": payload,
            }
        )
        db.session.add(event_log)
        db.session.flush()

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
            # the event handlers should not commit/rollback; the dispatcher should handle that
            # just flush results in the handlers
            result = event_handler(
                payload=data, plan_id=kwargs.get("parent_id"), **kwargs
            )
            cls.log_event(event, data)
            db.session.commit()
            return {"status": "success", "data": result}, 200
        except (PayloadValidationError, PlanInvalidError, IntegrityError) as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 400
        except NotAuthorizedError as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 403
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 500
