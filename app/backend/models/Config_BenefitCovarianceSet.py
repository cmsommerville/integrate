from app.extensions import db
from app.shared import BaseModel, BaseRowLevelSecurityTable
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from ..tables import TBL_NAMES

CONFIG_BENEFIT_COVARIANCE_SET = TBL_NAMES['CONFIG_BENEFIT_COVARIANCE_SET']
CONFIG_BENEFIT_COVARIANCE_SET_ACL = TBL_NAMES['CONFIG_BENEFIT_COVARIANCE_SET_ACL']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigBenefitCovarianceSet_ACL(BaseModel, BaseRowLevelSecurityTable):
    __tablename__ = CONFIG_BENEFIT_COVARIANCE_SET_ACL

    config_benefit_covariance_set_acl_id = db.Column(db.Integer, primary_key=True)
    config_benefit_covariance_set_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_COVARIANCE_SET}.config_benefit_covariance_set_id"))
    auth_role_code = db.Column(db.String(30), nullable=False)


class Model_ConfigBenefitCovarianceSet(BaseModel):
    __tablename__ = CONFIG_BENEFIT_COVARIANCE_SET

    config_benefit_covariance_set_id = db.Column(db.Integer, primary_key=True)
    config_benefit_product_variation_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_PRODUCT_VARIATION}.config_benefit_product_variation_id"), nullable=False)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    ref_optionality_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)

    acl = db.relationship("Model_ConfigBenefitCovarianceSet_ACL", 
        innerjoin=True, lazy='joined')
    optionality = db.relationship("Model_RefOptionality")
    covariance_details = db.relationship("Model_ConfigBenefitCovarianceDetail")