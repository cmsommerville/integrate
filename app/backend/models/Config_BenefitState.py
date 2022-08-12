from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_STATE = TBL_NAMES['CONFIG_BENEFIT_STATE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']
REF_STATES = TBL_NAMES['REF_STATES']

class Model_ConfigBenefitState(BaseModel):
    __tablename__ = CONFIG_BENEFIT_STATE
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'ref_benefit_id', 'state_id', 'config_benefit_state_effective_date'),
        db.CheckConstraint('config_benefit_state_effective_date <= config_benefit_state_expiration_date')
    )

    config_benefit_state_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"
    ))
    ref_benefit_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    state_id = db.Column(db.ForeignKey(
        f"{REF_STATES}.state_id"), nullable=False)
    config_benefit_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT}.config_benefit_id"), nullable=False)
    config_benefit_state_effective_date = db.Column(db.Date, nullable=False)
    config_benefit_state_expiration_date = db.Column(db.Date, nullable=False)

    ref_benefit = db.relationship("Model_RefBenefit", 
        primaryjoin="Model_ConfigBenefitState.ref_benefit_id == Model_RefBenefit.ref_id")
    benefit = db.relationship("Model_ConfigBenefit")
    state =  db.relationship("Model_RefStates")