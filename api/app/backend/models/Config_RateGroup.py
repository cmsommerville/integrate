from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_RATE_GROUP = TBL_NAMES["CONFIG_RATE_GROUP"]


class Model_ConfigRateGroup(BaseModel):
    __tablename__ = CONFIG_RATE_GROUP

    config_rate_group_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(
        db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), nullable=False
    )
    config_rate_group_code = db.Column(db.String(30), nullable=False)
    config_rate_group_label = db.Column(db.String(100), nullable=False)
    unit_value = db.Column(db.Numeric(10, 2), default=1)
    apply_discretionary_factor = db.Column(db.Boolean, default=True)

    parent = db.relationship("Model_ConfigProduct")
