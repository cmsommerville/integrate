import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

SELECTION_AGE_BAND = TBL_NAMES['SELECTION_AGE_BAND']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionAgeBand(BaseModel):
    __tablename__ = SELECTION_AGE_BAND
    __table_args__ = (
        db.UniqueConstraint('selection_plan_id', 'lower_age_value',), 
        db.CheckConstraint('lower_age_value <= upper_age_value')
    )

    selection_age_band_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    lower_age_value = db.Column(db.Integer, nullable=False)
    upper_age_value = db.Column(db.Integer, nullable=False)