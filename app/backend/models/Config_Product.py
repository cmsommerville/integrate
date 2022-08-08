import datetime
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_AGE_DISTRIBUTION_SET']
CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']
CONFIG_ATTRIBUTE_SET = TBL_NAMES['CONFIG_ATTRIBUTE_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']

class Model_ConfigProduct(BaseModel):
    __tablename__ = CONFIG_PRODUCT
    __table_args__ = (
        db.UniqueConstraint('config_product_code', 'config_product_effective_date'),
    )

    config_product_id = db.Column(db.Integer, primary_key=True)
    config_product_code = db.Column(db.String(30), nullable=False)
    config_product_label = db.Column(db.String(100), nullable=False)
    config_product_effective_date = db.Column(db.Date, nullable=False)
    config_product_expiration_date = db.Column(db.Date, default=datetime.date(9999,12,31))

    product_issue_date = db.Column(db.Date)
    master_product_code = db.Column(db.String(30))
    form_code = db.Column(db.String(30))
    min_issue_age = db.Column(db.Integer, nullable=False)
    max_issue_age = db.Column(db.Integer, nullable=False)

    smoker_status_distribution_set_id = db.Column(db.ForeignKey(F'{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.config_attr_distribution_set_id'), 
        comment="Default distribution of smokers")
    smoker_status_rating_strategy_id = db.Column(db.ForeignKey(F'{REF_MASTER}.ref_id'), 
        comment="Indicates whether smoker status is used for rating, underwriting, or not at all. Allows for other strategies to be created.")
    smoker_status_attr_set_id = db.Column(db.ForeignKey(F'{CONFIG_ATTRIBUTE_SET}.config_attr_set_id'), 
        comment="Specifies which smoker status attributes are used with this product")
 
    gender_distribution_set_id = db.Column(db.ForeignKey(F'{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.config_attr_distribution_set_id'), 
        comment="Default distribution of genders")
    gender_rating_strategy_id = db.Column(db.ForeignKey(F'{REF_MASTER}.ref_id'),
        comment="Indicates whether gender is used for rating, underwriting, or not at all. Allows for other strategies to be created.")
    gender_attr_set_id = db.Column(db.ForeignKey(F'{CONFIG_ATTRIBUTE_SET}.config_attr_set_id'), 
        comment="Specifies which gender attributes are used with this product")
        
    age_distribution_set_id = db.Column(db.ForeignKey(F'{CONFIG_AGE_DISTRIBUTION_SET}.config_age_distribution_set_id'), 
        comment="Default distribution of ages at issue")
    age_rating_strategy_id = db.Column(db.ForeignKey(F'{REF_MASTER}.ref_id'),
        comment="Indicates whether age is used for rating, underwriting, or not at all. Allows for other strategies to be created.")

    allow_employer_paid = db.Column(db.Boolean, nullable=False)
    voluntary_census_strategy_id = db.Column(db.ForeignKey(F"{REF_MASTER}.ref_id"), nullable=False, 
        comment="Indicates a specific strategy for handling custom censuses for voluntary quotes")
    employer_paid_census_strategy_id = db.Column(db.ForeignKey(F"{REF_MASTER}.ref_id"), nullable=False, 
        comment="Indicates a specific strategy for handling custom censuses for employer paid quotes")


    # product_variations = db.relationship(
    #     "Model_ConfigProductVariation", back_populates="product")
    # benefits = db.relationship(
    #     "Model_ConfigBenefit", back_populates="product")
    # provisions = db.relationship(
    #     "Model_ConfigProvision", back_populates="product")
    states = db.relationship("Model_ConfigProductState")