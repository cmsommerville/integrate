from app.backend.models.Config_Product import REF_MASTER
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
CONFIG_PROVISION_STATE = TBL_NAMES['CONFIG_PROVISION_STATE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']
REF_STATES = TBL_NAMES['REF_STATES']

class Model_ConfigProvisionState(BaseModel):
    __tablename__ = CONFIG_PROVISION_STATE
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'ref_provision_id', 'state_id', 'config_provision_state_effective_date'),
        db.CheckConstraint('config_provision_state_effective_date <= config_provision_state_expiration_date')
    )

    config_provision_state_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"
    ))
    ref_provision_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"
    ))
    state_id = db.Column(db.ForeignKey(
        f"{REF_STATES}.state_id"), nullable=False)

    config_provision_id = db.Column(db.ForeignKey(
        f"{CONFIG_PROVISION}.config_provision_id"), nullable=False)
    config_provision_state_effective_date = db.Column(db.Date, nullable=False)
    config_provision_state_expiration_date = db.Column(db.Date, nullable=False)

    provision = db.relationship("Model_ConfigProvision")
    state = db.relationship("Model_RefStates")
    ref_provision = db.relationship("Model_RefProvision",
        primaryjoin="Model_ConfigProvisionState.ref_provision_id == Model_RefProvision.ref_id")