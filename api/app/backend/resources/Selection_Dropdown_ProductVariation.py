import datetime
from marshmallow import Schema, fields
from sqlalchemy.sql import and_
from app.extensions import db
from app.shared.utils import system_temporal_hint
from ..models import (
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_SelectionPlan,
    Model_RefStates,
)


class DDSchema_ConfigProductVariationState(Schema):
    config_product_variation_state_id = fields.Integer()
    config_product_variation_id = fields.Integer()
    config_product_variation_code = fields.String()
    config_product_variation_label = fields.String()
    config_product_variation_state_effective_date = fields.Date()
    config_product_variation_state_expiration_date = fields.Date()
    state_code = fields.String()
    state_name = fields.String()
    version_id = fields.String()


class Selection_RPC_Dropdown_ProductVariation:
    schema = DDSchema_ConfigProductVariationState()

    def __init__(self, plan_id: int, t: datetime.datetime, *args, **kwargs):
        self.plan_id = plan_id
        self.t = t

    def get_product_variation_state_list(self, *args, **kwargs):
        """
        Get all product variations for a plan's product and state as of a given datetime
        """
        hint = system_temporal_hint(self.t)
        PV = Model_ConfigProductVariation
        PVS = Model_ConfigProductVariationState
        SP = Model_SelectionPlan
        ST = Model_RefStates

        objs = (
            db.session.query(
                PVS.config_product_variation_state_id,
                PVS.config_product_variation_id,
                PV.config_product_variation_code,
                PV.config_product_variation_label,
                PVS.config_product_variation_state_effective_date,
                PVS.config_product_variation_state_expiration_date,
                ST.state_code,
                ST.state_name,
                PVS.version_id,
            )
            .join(PV, PVS.config_product_variation_id == PV.config_product_variation_id)
            .join(ST, PVS.state_id == ST.state_id)
            .join(
                SP,
                and_(
                    PVS.state_id == SP.situs_state_id,
                    PV.config_product_id == SP.config_product_id,
                    PVS.config_product_variation_state_effective_date
                    <= SP.selection_plan_effective_date,
                    PVS.config_product_variation_state_expiration_date
                    >= SP.selection_plan_effective_date,
                ),
            )
            .with_hint(PVS, hint)
            .with_hint(PV, hint)
            .with_hint(ST, hint)
            .filter(SP.selection_plan_id == self.plan_id)
            .all()
        )

        return self.schema.dump(objs, many=True)
