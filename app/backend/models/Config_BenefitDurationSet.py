from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_DURATION_SET = TBL_NAMES['CONFIG_BENEFIT_DURATION_SET']


class Model_ConfigBenefitDurationSet(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_SET

    config_benefit_duration_set_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT}.config_benefit_id"), nullable=False)
    config_benefit_duration_set_code = db.Column(db.String(30), nullable=False)
    config_benefit_duration_set_label = db.Column(db.String(100), nullable=False)
    default_config_benefit_duration_detail_id = db.Column(db.Integer, nullable=True)

    duration_items = db.relationship("Model_ConfigBenefitDurationDetail")
    default_item = db.relationship("Model_ConfigBenefitDurationDetail",
        foreign_keys=[default_config_benefit_duration_detail_id], 
        primaryjoin="Model_ConfigBenefitDurationSet.default_config_benefit_duration_detail_id == Model_ConfigBenefitDurationDetail.config_benefit_duration_detail_id")