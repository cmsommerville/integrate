import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
SELECTION_CENSUS_DETAIL = TBL_NAMES['SELECTION_CENSUS_DETAIL']
SELECTION_CENSUS_SET = TBL_NAMES['SELECTION_CENSUS_SET']

class Model_SelectionCensusDetail(BaseModel):
    __tablename__ = SELECTION_CENSUS_DETAIL
    __table_args__ = (
        db.UniqueConstraint('selection_census_set_id', 'config_gender_detail_id', 'config_smoker_status_detail_id', 'age_value'), 
    )

    selection_census_detail_id = db.Column(db.Integer, primary_key=True)
    selection_census_set_id = db.Column(db.ForeignKey(f"{SELECTION_CENSUS_SET}.selection_census_set_id"))
    config_gender_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_smoker_status_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    age_value = db.Column(db.Integer, nullable=False)
    selection_census_weight = db.Column(db.Numeric(13, 5))

    gender = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_SelectionCensusDetail.config_gender_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    smoker_status = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_SelectionCensusDetail.config_smoker_status_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")