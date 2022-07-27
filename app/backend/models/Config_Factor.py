from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']


class Model_ConfigFactor(BaseModel):
    __tablename__ = CONFIG_FACTOR

    config_factor_id = db.Column(db.Integer, primary_key=True)
    config_provision_id = db.Column(db.ForeignKey(
        f"{CONFIG_PROVISION}.config_provision_id"
    ))
    factor_priority = db.Column(db.Integer, nullable=False)
    factor_value = db.Column(db.Numeric(8,5), nullable=False)
