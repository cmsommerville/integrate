from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_DURATION_DETAIL = TBL_NAMES['CONFIG_BENEFIT_DURATION_DETAIL']
CONFIG_BENEFIT_DURATION_SET = TBL_NAMES['CONFIG_BENEFIT_DURATION_SET']


class Model_ConfigBenefitDurationDetail(BaseModel):
    __tablename__ = CONFIG_BENEFIT_DURATION_DETAIL

    config_benefit_duration_detail_id = db.Column(db.Integer, primary_key=True)
    config_benefit_duration_set_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_DURATION_SET}.config_benefit_duration_set_id"), nullable=False)
    config_benefit_duration_detail_code = db.Column(db.String(30), nullable=False)
    config_benefit_duration_detail_label = db.Column(db.String(100), nullable=False)
    config_benefit_duration_factor = db.Column(db.Numeric(8,5), nullable=False)
