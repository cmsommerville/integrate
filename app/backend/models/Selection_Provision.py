import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_PROVISION = TBL_NAMES['CONFIG_BENEFIT_PROVISION']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionProvision(BaseModel):
    __tablename__ = SELECTION_PROVISION
    __table_args__ = (
        db.UniqueConstraint('selection_plan_id', 'config_provision_id', ), 
    )

    selection_provision_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    config_provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.config_provision_id"), nullable=False)
    selection_provision_value = db.Column(db.String(255), nullable=False)
