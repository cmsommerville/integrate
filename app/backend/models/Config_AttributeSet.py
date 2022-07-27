from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_SET = TBL_NAMES['CONFIG_ATTRIBUTE_SET']

class Model_ConfigAttributeSet(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_SET

    config_attr_set_id = db.Column(db.Integer, primary_key=True)
    config_attr_type_code = db.Column(db.String(30), nullable=False)
    config_attr_set_label = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_on': config_attr_type_code,
        'polymorphic_identity': 'attr_set'
    }



class Model_ConfigAttributeSet_Gender(Model_ConfigAttributeSet):
    __mapper_args__ = {
        'polymorphic_identity': 'gender'
    }

    genders = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigAttributeSet_Gender.config_attr_set_id == Model_ConfigAttributeDetail.config_attr_set_id")


class Model_ConfigAttributeSet_SmokerStatus(Model_ConfigAttributeSet):
    __mapper_args__ = {
        'polymorphic_identity': 'smoker_status'
    }

    smoker_statuses = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigAttributeSet_Gender.config_attr_set_id == Model_ConfigAttributeDetail.config_attr_set_id")


class Model_ConfigAttributeSet_Relationship(Model_ConfigAttributeSet):
    __mapper_args__ = {
        'polymorphic_identity': 'relationship'
    }

    relationships = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigAttributeSet_Relationship.config_attr_set_id == Model_ConfigAttributeDetail.config_attr_set_id")

