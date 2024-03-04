from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
SELECTION_BENEFIT = TBL_NAMES["SELECTION_BENEFIT"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionBenefit(BaseModel):
    __tablename__ = SELECTION_BENEFIT
    __table_args__ = (
        db.UniqueConstraint("selection_plan_id", "config_benefit_variation_state_id"),
    )

    selection_benefit_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    config_benefit_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_VARIATION_STATE}.config_benefit_variation_state_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    selection_value = db.Column(db.Numeric(12, 2), nullable=False)

    config_benefit_variation_state = db.relationship(
        "Model_ConfigBenefitVariationState"
    )

    @classmethod
    def find_by_plan(cls, selection_plan_id: int):
        return cls.query.filter(cls.selection_plan_id == selection_plan_id)
