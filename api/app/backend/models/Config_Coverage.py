from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_COVERAGE = TBL_NAMES["CONFIG_COVERAGE"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]


class Model_ConfigCoverage(BaseModel):
    __tablename__ = CONFIG_COVERAGE

    config_coverage_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(
        db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), nullable=False
    )
    config_coverage_code = db.Column(db.String(30), nullable=False)
    config_coverage_label = db.Column(db.String(100), nullable=False)
    config_coverage_description = db.Column(db.String(1000), nullable=False)

    parent = db.relationship("Model_ConfigProduct")
    benefits = db.relationship("Model_ConfigBenefit")
