import datetime
from app.extensions import db
from app.shared import BaseModel, BaseRowLevelSecurityTable

from ..tables import TBL_NAMES

CONFIG_DROPDOWN_DETAIL_ACL = TBL_NAMES["CONFIG_DROPDOWN_DETAIL_ACL"]
CONFIG_DROPDOWN_DETAIL = TBL_NAMES["CONFIG_DROPDOWN_DETAIL"]
CONFIG_DROPDOWN_SET = TBL_NAMES["CONFIG_DROPDOWN_SET"]


class Model_ConfigDropdownDetail_ACL(BaseModel, BaseRowLevelSecurityTable):
    __tablename__ = CONFIG_DROPDOWN_DETAIL_ACL

    config_dropdown_detail_acl_id = db.Column(db.Integer, primary_key=True)
    config_dropdown_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_DROPDOWN_DETAIL}.config_dropdown_detail_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    auth_role_code = db.Column(db.String(30), nullable=False)


class Model_ConfigDropdownDetail(BaseModel):
    __tablename__ = CONFIG_DROPDOWN_DETAIL
    __table_args__ = (
        db.UniqueConstraint(
            "config_dropdown_set_id",
            "config_dropdown_detail_code",
        ),
    )

    config_dropdown_detail_id = db.Column(db.Integer, primary_key=True)
    config_dropdown_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_DROPDOWN_SET}.config_dropdown_set_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
    )
    config_dropdown_detail_code = db.Column(db.String(30), nullable=False)
    config_dropdown_detail_label = db.Column(db.String(100), nullable=False)
    is_restricted = db.Column(db.Boolean, default=False)

    acl = db.relationship("Model_ConfigDropdownDetail_ACL", lazy="joined")
