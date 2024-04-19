from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_BENEFIT_DURATION_DETAIL = TBL_NAMES["CONFIG_BENEFIT_DURATION_DETAIL"]
CONFIG_BENEFIT_DURATION_SET = TBL_NAMES["CONFIG_BENEFIT_DURATION_SET"]
SELECTION_BENEFIT = TBL_NAMES["SELECTION_BENEFIT"]
SELECTION_BENEFIT_DURATION = TBL_NAMES["SELECTION_BENEFIT_DURATION"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionBenefitDuration(BaseModel):
    __tablename__ = SELECTION_BENEFIT_DURATION
    __table_args__ = (
        db.UniqueConstraint("selection_benefit_id", "config_benefit_duration_set_id"),
    )

    selection_benefit_duration_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_BENEFIT}.selection_benefit_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    config_benefit_duration_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_DURATION_SET}.config_benefit_duration_set_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    config_benefit_duration_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_DURATION_DETAIL}.config_benefit_duration_detail_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    selection_factor = db.Column(db.Numeric(8, 5), default=1)

    config_benefit_duration_detail = db.relationship(
        "Model_ConfigBenefitDurationDetail"
    )
