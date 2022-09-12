import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']
SELECTION_BENEFIT = TBL_NAMES['SELECTION_BENEFIT']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionBenefit(BaseModel):
    __tablename__ = SELECTION_BENEFIT
    __table_args__ = (
        db.UniqueConstraint('selection_plan_id', 'config_benefit_product_variation_id',), 
    )

    selection_benefit_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    config_benefit_product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_BENEFIT_PRODUCT_VARIATION}.config_benefit_product_variation_id"), nullable=False)
    config_benefit_id =  db.Column(db.ForeignKey(f"{CONFIG_BENEFIT}.config_benefit_id"))
    selection_benefit_value = db.Column(db.Numeric(12, 2), nullable=False)

    config_benefit =  db.relationship("Model_ConfigBenefit", 
        primaryjoin="Model_SelectionBenefit.config_benefit_id == Model_ConfigBenefit.config_benefit_id")

    config_rate_tables = db.relationship("Model_ConfigRateTable", 
        foreign_keys=[config_benefit_product_variation_id],
        primaryjoin="Model_SelectionBenefit.config_benefit_product_variation_id == Model_ConfigRateTable.config_benefit_product_variation_id")

    @classmethod
    def find_by_plan(cls, plan_id: int): 
        return cls.query.filter(cls.selection_plan_id==plan_id).all()
