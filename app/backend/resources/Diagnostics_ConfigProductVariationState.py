from flask import request
from flask_restx import Resource
from ..classes.Diagnostics_ConfigProductVariationState import (
    Diagnostics_ConfigProductVariationState,
)
from app.auth import authorization_required


class Resource_Diagnostics_ConfigProductVariationState(Resource):
    permissions = {
        "get": ["*"],
    }

    @classmethod
    @authorization_required
    def get(cls, id: int, *args, **kwargs):
        try:
            data = Diagnostics_ConfigProductVariationState.diagnostics_benefit_variation_state(
                id
            )
            return data, 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400


class Resource_Diagnostics_ConfigProductVariation(Resource):
    permissions = {
        "get": ["*"],
    }

    @classmethod
    @authorization_required
    def get(cls, id: int, *args, **kwargs):
        try:
            data = Diagnostics_ConfigProductVariationState.diagnostics_benefit_variation_states_all(
                id
            )
            return data, 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
