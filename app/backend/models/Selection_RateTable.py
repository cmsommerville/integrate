from typing import List
from sqlalchemy.sql import text
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
SELECTION_AGE_BAND = TBL_NAMES['SELECTION_AGE_BAND']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']
SELECTION_RATE_TABLE = TBL_NAMES['SELECTION_RATE_TABLE']



class Model_SelectionRateTable(BaseModel):
    __tablename__ = SELECTION_RATE_TABLE

    selection_rate_table_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"))
    selection_age_band_id = db.Column(db.ForeignKey(f'{SELECTION_AGE_BAND}.selection_age_band_id'))
    config_rate_group_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_GROUP}.config_rate_group_id'))
    config_gender_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    config_smoker_status_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    config_relationship_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    annual_rate = db.Column(db.Numeric(12,5), default=0)
    discretionary_factor = db.Column(db.Numeric(8,5), default=1)

    config_rate_group = db.relationship("Model_ConfigRateGroup")
    age_band = db.relationship("Model_SelectionAgeBand")
    gender = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_SelectionRateTable.config_gender_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    smoker_status = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_SelectionRateTable.config_smoker_status_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    relationship = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_SelectionRateTable.config_relationship_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")

    @classmethod
    def find_by_plan(cls, plan_id: int):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()
