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
SELECTION_BENEFIT_RATE_TABLE = TBL_NAMES['SELECTION_BENEFIT_RATE_TABLE']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']



class Model_SelectionBenefitRateTable(BaseModel):
    __tablename__ = SELECTION_BENEFIT_RATE_TABLE

    selection_benefit_rate_table_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"))
    selection_benefit_id = db.Column(db.ForeignKey(f"{SELECTION_BENEFIT}.selection_benefit_id"))
    selection_age_band_id = db.Column(db.ForeignKey(f'{SELECTION_AGE_BAND}.selection_age_band_id'))
    config_rate_group_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_GROUP}.config_rate_group_id'))
    config_gender_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    config_smoker_status_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    config_relationship_detail_id = db.Column(db.ForeignKey(f'{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id'))
    annual_rate = db.Column(db.Numeric(12,5), default=0)

    @classmethod
    def find_by_plan(cls, plan_id: int):
        return cls.query.filter(cls.selection_plan_id == plan_id).all()

    @classmethod
    def create_rate_table(cls, plan_id: int): 
        stmt = text('EXEC sp_selection_rate_calc :plan_id')
        try: 
            res = db.session.execute(stmt, {'plan_id': plan_id})
            db.session.commit()
        except: 
            db.session.rollback()
            raise
    
    
