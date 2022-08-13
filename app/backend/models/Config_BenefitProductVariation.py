from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES['CONFIG_BENEFIT']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']
CONFIG_PRODUCT_VARIATION = TBL_NAMES['CONFIG_PRODUCT_VARIATION']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigBenefitProductVariation(BaseModel):
    __tablename__ = CONFIG_BENEFIT_PRODUCT_VARIATION
    __table_args__ = (
        db.UniqueConstraint('config_benefit_id', 'config_product_variation_id'),
    )

    config_benefit_product_variation_id = db.Column(db.Integer, primary_key=True)
    config_benefit_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT}.config_benefit_id"), nullable=False)
    config_product_variation_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT_VARIATION}.config_product_variation_id"), nullable=False)
    is_enabled = db.Column(db.Boolean, default=False)

    benefit = db.relationship("Model_ConfigBenefit")
    product_variation = db.relationship("Model_ConfigProductVariation")