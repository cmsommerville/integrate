from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

SELECTION_AGE_BAND = TBL_NAMES["SELECTION_AGE_BAND"]
SELECTION_BENEFIT = TBL_NAMES["SELECTION_BENEFIT"]
SELECTION_BENEFIT_RATE = TBL_NAMES["SELECTION_BENEFIT_RATE"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionBenefitRate(BaseModel):
    __tablename__ = SELECTION_BENEFIT_RATE

    selection_benefit_rate_id = db.Column(db.Integer, primary_key=True)
    selection_benefit_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_BENEFIT}.selection_benefit_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
        ),
        index=True,
    )
    selection_age_band_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_AGE_BAND}.selection_age_band_id",
        ),
        index=True,
    )
    output_attribute_detail_id1 = db.Column(db.Integer, default=-1)
    output_attribute_detail_id2 = db.Column(db.Integer, default=-1)
    output_attribute_detail_id3 = db.Column(db.Integer, default=-1)
    output_attribute_detail_id4 = db.Column(db.Integer, default=-1)
    output_attribute_detail_id5 = db.Column(db.Integer, default=-1)
    output_attribute_detail_id6 = db.Column(db.Integer, default=-1)
    rate = db.Column(db.Numeric(12, 5), default=1)
