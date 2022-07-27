from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION

    config_provision_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    ref_provision_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    is_rate_table_factor = db.Column(db.Boolean, default=False)
    config_provision_description = db.Column(db.String(1000))

    ui_component = db.relationship("Model_ConfigProvisionUI")
    ref_benefit = db.relationship("Model_RefMaster",
        primaryjoin="Model_ConfigProvision.ref_provision_id == Model_RefMaster.ref_id")
