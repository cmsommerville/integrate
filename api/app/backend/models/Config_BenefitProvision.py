from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_BENEFIT_PROVISION = TBL_NAMES["CONFIG_BENEFIT_PROVISION"]
CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigBenefitProvision(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PROVISION
    __table_args__ = (db.UniqueConstraint("config_benefit_id", "config_provision_id"),)

    config_benefit_provision_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(
        db.ForeignKey(f"{CONFIG_BENEFIT}.config_benefit_id"), nullable=False
    )
    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION}.config_provision_id"), nullable=False
    )
    is_enabled = db.Column(db.Boolean, default=True)

    benefit = db.relationship("Model_ConfigBenefit")
    provision = db.relationship("Model_ConfigProvision")
