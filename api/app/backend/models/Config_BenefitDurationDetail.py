from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_DURATION_DETAIL_AUTH_ACL = TBL_NAMES[
    "CONFIG_BENEFIT_DURATION_DETAIL_AUTH_ACL"
]
CONFIG_BENEFIT_DURATION_DETAIL = TBL_NAMES["CONFIG_BENEFIT_DURATION_DETAIL"]
CONFIG_BENEFIT_DURATION_SET = TBL_NAMES["CONFIG_BENEFIT_DURATION_SET"]


class Model_ConfigBenefitDurationDetailAuth_ACL(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_DETAIL_AUTH_ACL
    __table_args__ = ({"info": {"rls": "user_role"}},)

    config_benefit_duration_detail_auth_acl_id = db.Column(db.Integer, primary_key=True)
    config_benefit_duration_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_DURATION_DETAIL}.config_benefit_duration_detail_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    auth_role_code = db.Column(db.String(30), nullable=False)


class Model_ConfigBenefitDurationDetail(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_DETAIL

    config_benefit_duration_detail_id = db.Column(db.Integer, primary_key=True)
    config_benefit_duration_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_DURATION_SET}.config_benefit_duration_set_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    )
    config_benefit_duration_detail_code = db.Column(db.String(30), nullable=False)
    config_benefit_duration_detail_label = db.Column(db.String(100), nullable=False)
    config_benefit_duration_factor = db.Column(db.Numeric(8, 5), nullable=False)
    is_restricted = db.Column(db.Boolean, default=False)

    acl = db.relationship("Model_ConfigBenefitDurationDetailAuth_ACL", lazy="joined")
    parent = db.relationship("Model_ConfigBenefitDurationSet")
