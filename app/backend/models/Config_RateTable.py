from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_BENEFIT_PRODUCT_VARIATION = TBL_NAMES['CONFIG_BENEFIT_PRODUCT_VARIATION']
CONFIG_RATE_TABLE = TBL_NAMES['CONFIG_RATE_TABLE']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigRateTable(BaseModel):
    __tablename__ = CONFIG_RATE_TABLE

    config_rate_table_id = db.Column(db.Integer, primary_key=True)
    config_benefit_product_variation_id = db.Column(db.ForeignKey(
        f"{CONFIG_BENEFIT_PRODUCT_VARIATION}.config_benefit_product_variation_id"), nullable=False)
    age_value = db.Column(db.Integer, nullable=False)
    config_gender_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_smoker_status_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_relationship_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    
    annual_rate_per_unit = db.Column(db.Numeric(12, 5), nullable=False)
    unit_value = db.Column(db.Numeric(12, 2), nullable=False)

    benefit_product_variation = db.relationship("Model_ConfigBenefitProductVariation")
    gender = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigRateTable.config_gender_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    smoker_status = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigRateTable.config_smoker_status_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    relationship = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigRateTable.config_relationship_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")