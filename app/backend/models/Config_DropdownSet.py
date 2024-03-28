import datetime
from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_

from ..tables import TBL_NAMES
from .Config_DropdownDetail import (
    Model_ConfigDropdownDetail,
    Model_ConfigDropdownDetail_ACL,
)

CONFIG_DROPDOWN_SET = TBL_NAMES["CONFIG_DROPDOWN_SET"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigDropdownSet(BaseModel):
    __tablename__ = CONFIG_DROPDOWN_SET

    config_dropdown_set_id = db.Column(db.Integer, primary_key=True)
    config_dropdown_set_label = db.Column(db.String(100), unique=True, nullable=False)
    is_numeric = db.Column(db.Boolean, default=False)
    detail_display_strategy_code = db.Column(db.String(30), nullable=False)
    sort_by_code = db.Column(db.Boolean, default=False)

    _dropdown_details = db.relationship("Model_ConfigDropdownDetail")

    @hybrid_property
    def dropdown_details(self):
        DD = Model_ConfigDropdownDetail
        ACL = Model_ConfigDropdownDetail_ACL
        data = (
            db.session.query(DD)
            .filter(
                DD.config_dropdown_set_id == self.config_dropdown_set_id,
                or_(
                    DD.is_restricted == False,
                    db.session.query(ACL)
                    .filter(
                        ACL.config_dropdown_detail_id == DD.config_dropdown_detail_id
                    )
                    .count()
                    > 0,
                ),
            )
            .all()
        )
        return data

    @dropdown_details.setter
    def dropdown_details(self, values):
        self._dropdown_details = values
