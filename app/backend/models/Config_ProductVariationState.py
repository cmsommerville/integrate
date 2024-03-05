import datetime
from app.extensions import db
from app.shared import BaseModel

from .Config_ProductVariation import Model_ConfigProductVariation
from .Ref_States import Model_RefStates
from ..tables import TBL_NAMES

CONFIG_AGE_BAND_SET = TBL_NAMES["CONFIG_AGE_BAND_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]
CONFIG_PRODUCT_VARIATION = TBL_NAMES["CONFIG_PRODUCT_VARIATION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]


class Model_ConfigProductVariationState(BaseModel):
    __tablename__ = CONFIG_PRODUCT_VARIATION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_product_variation_id",
            "state_id",
            "config_product_variation_state_effective_date",
        ),
        db.CheckConstraint(
            "config_product_variation_state_effective_date <= config_product_variation_state_expiration_date"
        ),
    )

    config_product_variation_state_id = db.Column(db.Integer, primary_key=True)
    config_product_variation_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION}.config_product_variation_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"))

    config_product_variation_state_effective_date = db.Column(db.Date, nullable=False)
    config_product_variation_state_expiration_date = db.Column(db.Date, nullable=False)
    default_config_age_band_set_id = db.Column(
        db.ForeignKey(f"{CONFIG_AGE_BAND_SET}.config_age_band_set_id")
    )

    age_band_set = db.relationship("Model_ConfigAgeBandSet")
    state = db.relationship("Model_RefStates")

    @classmethod
    def find_by_product_variation(cls, id):
        return cls.query.filter(cls.config_product_variation_id == id).all()

    @classmethod
    def find_one_for_selection_plan(
        cls,
        config_product_id: int,
        config_product_variation_code: str,
        state_code: str,
        plan_effective_date: datetime.date,
    ):
        PV = Model_ConfigProductVariation
        S = Model_RefStates
        return (
            db.session.query(cls)
            .join(PV, cls.config_product_variation_id == PV.config_product_variation_id)
            .join(S, cls.state_id == S.state_id)
            .filter(
                PV.config_product_variation_code == config_product_variation_code,
                PV.config_product_id == config_product_id,
                S.state_code == state_code,
                cls.config_product_variation_state_effective_date
                <= plan_effective_date,
                plan_effective_date
                <= cls.config_product_variation_state_expiration_date,
            )
            .order_by(cls.config_product_variation_state_effective_date.desc())
            .one()
        )
