from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']

class Model_ConfigAttributeDistributionSet(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_DISTRIBUTION_SET

    config_attr_distribution_set_id = db.Column(db.Integer, primary_key=True)
    config_attr_type_code = db.Column(db.String(30), nullable=False)
    config_attr_distribution_set_label = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_on': config_attr_type_code,
        'polymorphic_identity': 'attr_dist_set'
    }


class Model_ConfigAttributeDistributionSet_Gender(Model_ConfigAttributeDistributionSet): 
    gender_distribution = db.relationship("Model_ConfigAttributeDistribution", 
        primaryjoin="Model_ConfigAttributeDistributionSet_Gender.config_attr_distribution_set_id == Model_ConfigAttributeDistribution.config_attr_distribution_set_id")

    __mapper_args__ = {
        'polymorphic_identity': 'gender'
    }


class Model_ConfigAttributeDistributionSet_SmokerStatus(Model_ConfigAttributeDistributionSet): 
    smoker_status_distribution = db.relationship("Model_ConfigAttributeDistribution", 
        primaryjoin="Model_ConfigAttributeDistributionSet_SmokerStatus.config_attr_distribution_set_id == Model_ConfigAttributeDistribution.config_attr_distribution_set_id")
        
    __mapper_args__ = {
        'polymorphic_identity': 'smoker_status'
    }

