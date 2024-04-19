import datetime
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.auth import authorization_required, NotAuthorizedError
from app.shared.errors import PlanInvalidError
from app.extensions import db
from app.cache import cachedmethod

from ..models import Model_SelectionPlan

from .Selection_Dropdown_ProductVariation import Selection_RPC_Dropdown_ProductVariation


SELECTION_DROPDOWN_MAPPER = {
    "variation-states": (
        Selection_RPC_Dropdown_ProductVariation,
        "get_product_variation_state_list",
    ),
}


class PayloadValidationError(Exception):
    pass


class Resource_Selection_RPC_Dropdown_Dispatcher(Resource):
    events = SELECTION_DROPDOWN_MAPPER
    permissions = {"get": ["read:selection"]}

    @classmethod
    @cachedmethod()
    def get_as_of_dts(cls, plan_id: int):
        plan = (
            db.session.query(Model_SelectionPlan.plan_as_of_dts)
            .filter_by(selection_plan_id=plan_id)
            .one()
        )
        return plan[0].strftime("%Y-%m-%d %H:%M:%S.%f")

    @classmethod
    @authorization_required
    def get(cls, parent_id: int, event: str, *args, **kwargs):
        try:
            if event not in cls.events:
                raise PayloadValidationError("Invalid event")
            event_class, event_method = cls.events[event]
            if event_class is None:
                raise ValueError("Event handler not implemented")

            t = datetime.datetime.strptime(
                cls.get_as_of_dts(parent_id), "%Y-%m-%d %H:%M:%S.%f"
            )

            instance = event_class(plan_id=parent_id, t=t, **kwargs)
            fn = getattr(instance, event_method)
            result = fn(**kwargs)
            return {"status": "success", "data": result}, 200
        except (
            ValidationError,
            PayloadValidationError,
            PlanInvalidError,
            IntegrityError,
        ) as e:
            return {"status": "error", "msg": str(e)}, 400
        except NotAuthorizedError as e:
            return {"status": "error", "msg": str(e)}, 403
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 500
