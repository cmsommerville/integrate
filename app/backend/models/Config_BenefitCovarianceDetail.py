from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT_COVARIANCE_DETAIL = TBL_NAMES['CONFIG_BENEFIT_COVARIANCE_DETAIL']
CONFIG_BENEFIT_COVARIANCE_SET = TBL_NAMES['CONFIG_BENEFIT_COVARIANCE_SET']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']



class Model_ConfigBenefitCovarianceDetail(BaseModel):
    __tablename__ = CONFIG_BENEFIT_COVARIANCE_DETAIL

    config_benefit_covariance_detail_id = db.Column(db.Integer, primary_key=True)
    config_benefit_covariance_set_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_COVARIANCE_SET}.config_benefit_covariance_set_id"))
    config_benefit_product_variation_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_PRODUCT_VARIATION}.config_benefit_product_variation_id"), nullable=False)
    