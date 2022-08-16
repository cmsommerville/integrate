import datetime
from sqlalchemy.sql.functions import current_timestamp
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
SELECTION_CENSUS_SET = TBL_NAMES['SELECTION_CENSUS_SET']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionCensusSet(BaseModel):
    __tablename__ = SELECTION_CENSUS_SET

    selection_census_set_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    selection_census_description = db.Column(db.String(255), default=f"Census uploaded at {current_timestamp()}")
    is_gender_distinct = db.Column(db.Boolean, nullable=False)
    is_smoker_status_distinct = db.Column(db.Boolean, nullable=False)
    is_age_distinct = db.Column(db.Boolean, nullable=False)

    census_details = db.relationship("Model_SelectionCensusDetail", 
        primaryjoin="Model_SelectionCensusSet.selection_census_set_id == Model_SelectionCensusDetail.selection_census_set_id")