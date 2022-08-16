import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_MAPPER_DETAIL = TBL_NAMES['CONFIG_AGE_MAPPER_DETAIL']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_MAPPER_SET =  TBL_NAMES['CONFIG_PRODUCT_MAPPER_SET']
CONFIG_PRODUCT_VARIATION = TBL_NAMES['CONFIG_PRODUCT_VARIATION']
REF_MASTER = TBL_NAMES['REF_MASTER']
REF_STATES = TBL_NAMES['REF_STATES']
SELECTION_CENSUS_SET = TBL_NAMES['SELECTION_CENSUS_SET']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionPlan(BaseModel):
    __tablename__ = SELECTION_PLAN

    selection_plan_id = db.Column(db.Integer, primary_key=True)
    selection_plan_effective_date = db.Column(db.Date)
    state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"), nullable=False)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    config_product_variation_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_VARIATION}.config_product_variation_id"), nullable=False)
    config_gender_product_mapper_set_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_MAPPER_SET}.config_product_mapper_set_id"), nullable=False)
    config_smoker_status_product_mapper_set_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_MAPPER_SET}.config_product_mapper_set_id"), nullable=False)
    is_employer_paid = db.Column(db.Boolean, default=False)
    selection_census_set_id = db.Column(db.Integer, nullable=True)
    selection_group_id = db.Column(db.Integer)
    selection_broker_id = db.Column(db.Integer)
    selection_plan_description = db.Column(db.String(255))
    is_template_indicator = db.Column(db.Boolean, default=False)
    cloned_selection_plan_id = db.Column(db.Integer, db.ForeignKey(f'{SELECTION_PLAN}.selection_plan_id'))
    discretionary_factor = db.Column(db.Numeric(8, 5))

    state = db.relationship("Model_RefStates")