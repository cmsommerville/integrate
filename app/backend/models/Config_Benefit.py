from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_COVERAGE = TBL_NAMES['CONFIG_COVERAGE']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigBenefit(BaseModel):
    __tablename__ = CONFIG_BENEFIT
    __table_args__ = (
        db.UniqueConstraint('config_benefit_version_code'),
    )

    config_benefit_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    ref_benefit_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    config_coverage_id = db.Column(db.ForeignKey(
        f"{CONFIG_COVERAGE}.config_coverage_id"))
    config_rate_group_id = db.Column(db.ForeignKey(
        f"{CONFIG_RATE_GROUP}.config_rate_group_id"))
    config_benefit_version_code = db.Column(db.String(30), nullable=False)
    min_value = db.Column(db.Numeric(12, 2))
    max_value = db.Column(db.Numeric(12, 2))
    step_value = db.Column(db.Numeric(12, 4))
    default_value = db.Column(db.Numeric(12, 4))
    unit_type_id = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))
    is_durational = db.Column(db.Boolean)
    config_benefit_description = db.Column(db.String(1000))

    durations = db.relationship("Model_ConfigBenefitDurationSet")
    ref_benefit = db.relationship("Model_RefBenefit",
        primaryjoin="Model_ConfigBenefit.ref_benefit_id == Model_RefBenefit.ref_id")
    coverage = db.relationship("Model_ConfigCoverage")
    rate_group = db.relationship("Model_ConfigRateGroup")