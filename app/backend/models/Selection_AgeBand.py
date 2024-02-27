from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
SELECTION_AGE_BAND = TBL_NAMES["SELECTION_AGE_BAND"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionAgeBand(BaseModel):
    __tablename__ = SELECTION_AGE_BAND
    __table_args__ = (
        db.UniqueConstraint("selection_plan_id", "age_band_lower"),
        db.CheckConstraint("age_band_lower <= age_band_upper"),
    )

    selection_age_band_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    age_band_lower = db.Column(db.Integer, nullable=False)
    age_band_upper = db.Column(db.Integer, nullable=False)
