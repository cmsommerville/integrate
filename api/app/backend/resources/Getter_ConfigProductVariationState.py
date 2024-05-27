from flask import request
from flask_restx import Resource
from sqlalchemy import and_
from app.extensions import db
from ..models import (
    Model_ConfigProductVariationState,
    Model_ConfigProductVariation,
    Model_ConfigProductState,
    Model_RefStates,
)
from ..schemas import Schema_Getter_ConfigProductVariationState_SelectionPlan


class Getter_ConfigProductVariationState_SelectionPlan(Resource):
    schema = Schema_Getter_ConfigProductVariationState_SelectionPlan(many=True)

    @staticmethod
    def _qry_available_product_variation_states(
        config_product_id, selection_plan_effective_date
    ):
        PVS = Model_ConfigProductVariationState
        PV = Model_ConfigProductVariation
        PS = Model_ConfigProductState
        ST = Model_RefStates

        qry = (
            db.session.query(
                PVS.config_product_variation_state_id,
                PVS.config_product_variation_id,
                PV.config_product_variation_label,
                PVS.state_id,
                ST.state_code,
                ST.state_name,
            )
            .select_from(PVS)
            .join(PV, PVS.config_product_variation_id == PV.config_product_variation_id)
            .join(
                PS,
                and_(
                    PVS.state_id == PS.state_id,
                    PV.config_product_id == PS.config_product_id,
                ),
            )
            .join(ST, ST.state_id == PVS.state_id)
            .filter(
                PV.config_product_id == config_product_id,
                PVS.config_product_variation_state_effective_date
                <= selection_plan_effective_date,
                PVS.config_product_variation_state_expiration_date
                >= selection_plan_effective_date,
                PS.config_product_state_effective_date <= selection_plan_effective_date,
                PS.config_product_state_expiration_date
                >= selection_plan_effective_date,
            )
        )
        return qry.all()

    def get(self):
        try:
            config_product_id = request.args.get("pid")
            selection_plan_effective_date = request.args.get("dt")
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try:
            objs = self._qry_available_product_variation_states(
                config_product_id, selection_plan_effective_date
            )
            data = self.schema.dump(objs)
            return {"status": "success", "data": data}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500
