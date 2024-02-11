from app.extensions import db
from app.shared import BaseModel

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
