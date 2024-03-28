import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db
from app.shared import BaseModel
from .Config_Benefit import Model_ConfigBenefit
from .Config_Coverage import Model_ConfigCoverage

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]
CONFIG_RATE_TABLE_SET = TBL_NAMES["CONFIG_RATE_TABLE_SET"]
REF_STATES = TBL_NAMES["REF_STATES"]


class Model_ConfigBenefitVariationState(BaseModel):
    __tablename__ = CONFIG_BENEFIT_VARIATION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_benefit_id",
            "config_product_variation_state_id",
            "config_benefit_variation_state_effective_date",
        ),
        db.CheckConstraint(
            "config_benefit_variation_state_effective_date <= config_benefit_variation_state_expiration_date"
        ),
    )

    config_benefit_variation_state_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT}.config_benefit_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    config_product_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION_STATE}.config_product_variation_state_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        nullable=True,
    )
    state_id = db.Column(
        db.ForeignKey(
            f"{REF_STATES}.state_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        nullable=True,
    )
    config_benefit_variation_state_effective_date = db.Column(db.Date, nullable=False)
    config_benefit_variation_state_expiration_date = db.Column(db.Date, nullable=False)
    config_rate_table_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATE_TABLE_SET}.config_rate_table_set_id",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        nullable=True,
    )

    parent = db.relationship("Model_ConfigBenefit")
    state = db.relationship("Model_RefStates")
    rate_table_set = db.relationship("Model_ConfigRateTableSet")

    @classmethod
    def find_quotable_benefits(
        cls,
        config_product_variation_state_id: int,
        state_id: int,
        plan_effective_date: datetime.date,
        *args,
        **kwargs,
    ):
        B = Model_ConfigBenefit
        CVG = Model_ConfigCoverage
        data = (
            db.session.query(cls, B, CVG)
            .join(B, cls.config_benefit_id == B.config_benefit_id)
            .join(CVG, B.config_coverage_id == CVG.config_coverage_id)
            .filter(
                cls.config_product_variation_state_id
                == config_product_variation_state_id,
                cls.state_id == state_id,
                cls.config_benefit_variation_state_effective_date
                <= plan_effective_date,
                cls.config_benefit_variation_state_expiration_date
                >= plan_effective_date,
            )
            .all()
        )
        return data
