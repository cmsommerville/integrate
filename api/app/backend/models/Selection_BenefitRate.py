from app.extensions import db
from sqlalchemy.types import VARBINARY

from ..tables import TBL_NAMES

SELECTION_AGE_BAND = TBL_NAMES["SELECTION_AGE_BAND"]
SELECTION_BENEFIT = TBL_NAMES["SELECTION_BENEFIT"]
SELECTION_BENEFIT_RATE = TBL_NAMES["SELECTION_BENEFIT_RATE"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionBenefitRate(db.Model):
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
    rate_value = db.Column(db.Numeric(12, 5), default=1)
    row_hash = db.Column(VARBINARY(40))
    created_dts = db.Column(db.DateTime)
    updated_dts = db.Column(db.DateTime)
    updated_by = db.Column(db.String(50), default="UNKNOWN")
