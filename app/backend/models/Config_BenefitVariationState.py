from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_VARIATION = TBL_NAMES["CONFIG_BENEFIT_VARIATION"]
CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
CONFIG_RATE_TABLE_SET = TBL_NAMES["CONFIG_RATE_TABLE_SET"]
REF_STATES = TBL_NAMES["REF_STATES"]


class Model_ConfigBenefitVariationState(BaseModel):
    __tablename__ = CONFIG_BENEFIT_VARIATION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_benefit_variation_id",
            "state_id",
            "config_benefit_variation_state_effective_date",
        ),
        db.CheckConstraint(
            "config_benefit_variation_state_effective_date <= config_benefit_variation_state_expiration_date"
        ),
    )

    config_benefit_variation_state_id = db.Column(db.Integer, primary_key=True)
    config_benefit_variation_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_VARIATION}.config_benefit_variation_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"), nullable=False)
    config_benefit_variation_state_effective_date = db.Column(db.Date, nullable=False)
    config_benefit_variation_state_expiration_date = db.Column(db.Date, nullable=False)
    config_rate_table_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATE_TABLE_SET}.config_rate_table_set_id",
            onupdate="SET NULL",
            ondelete="SET NULL",
        )
    )

    benefit_variation = db.relationship("Model_ConfigBenefitVariation")
    state = db.relationship("Model_RefStates")
    rate_table_set = db.relationship("Model_ConfigRateTableSet")
