import pandas as pd
from sqlalchemy import func
from app.extensions import db
from ..models import (
    Model_ConfigProductVariationState,
    Model_ConfigBenefitVariationState,
    Model_RefStates,
)


class Diagnostics_ConfigProductVariationState:
    @classmethod
    def diagnostics_benefit_variation_state(
        cls, product_variation_state_id: int, *args, **kwargs
    ):
        PVS = Model_ConfigProductVariationState
        BVS = Model_ConfigBenefitVariationState
        ST = Model_RefStates
        df = pd.DataFrame(
            db.session.query(
                PVS.config_product_variation_state_id,
                ST.state_code,
                func.count(BVS.config_benefit_variation_state_id).label(
                    "count_benefit_variation_states"
                ),
                func.count(BVS.config_rate_table_set_id).label("count_rate_tables"),
            )
            .join(ST, PVS.state_id == ST.state_id)
            .join(
                BVS,
                PVS.config_product_variation_state_id
                == BVS.config_product_variation_state_id,
                isouter=True,
            )
            .filter(PVS.config_product_variation_state_id == product_variation_state_id)
            .group_by(PVS.config_product_variation_state_id, ST.state_code)
            .all()
        )
        return df.to_dict("records")

    @classmethod
    def diagnostics_benefit_variation_states_all(
        cls, product_variation_id: int, *args, **kwargs
    ):
        PVS = Model_ConfigProductVariationState
        BVS = Model_ConfigBenefitVariationState
        ST = Model_RefStates
        df = pd.DataFrame(
            db.session.query(
                PVS.config_product_variation_state_id,
                ST.state_code,
                func.count(BVS.config_benefit_variation_state_id).label(
                    "count_benefit_variation_states"
                ),
                func.count(BVS.config_rate_table_set_id).label("count_rate_tables"),
            )
            .join(ST, PVS.state_id == ST.state_id)
            .join(
                BVS,
                PVS.config_product_variation_state_id
                == BVS.config_product_variation_state_id,
                isouter=True,
            )
            .filter(PVS.config_product_variation_id == product_variation_id)
            .group_by(PVS.config_product_variation_state_id, ST.state_code)
            .all()
        )
        return df.to_dict("records")
