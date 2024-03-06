import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_DROPDOWN_SET = TBL_NAMES["CONFIG_DROPDOWN_SET"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigDropdownSet(BaseModel):
    __tablename__ = CONFIG_DROPDOWN_SET

    config_dropdown_set_id = db.Column(db.Integer, primary_key=True)
    config_dropdown_set_label = db.Column(db.String(100), unique=True, nullable=False)
    is_numeric = db.Column(db.Boolean, default=False)
    detail_display_strategy_code = db.Column(db.String(30), nullable=False)
    sort_by_code = db.Column(db.Boolean, default=False)

    dropdown_details = db.relationship("Model_ConfigDropdownDetail", lazy="joined")
