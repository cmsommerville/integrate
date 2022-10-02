from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT_MAPPER_SET = TBL_NAMES['CONFIG_PRODUCT_MAPPER_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_MASTER = TBL_NAMES['REF_MASTER']

class Model_ConfigProductMapperSet(BaseModel):
    __tablename__ = CONFIG_PRODUCT_MAPPER_SET
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'config_attr_type_code', 'config_attr_mapper_type_id'),
    )

    config_product_mapper_set_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f'{CONFIG_PRODUCT}.config_product_id'), nullable=False)
    config_attr_type_code = db.Column(db.String(30), nullable=False, 
        comment="Specifies the attribute type, such as gender or smoker status")
    config_attr_mapper_type_id = db.Column(db.ForeignKey(f'{REF_MASTER}.ref_id'), nullable=False,
        comment="Specifies the mapper type, such as composite or distinct")
    is_default = db.Column(db.Boolean, nullable=False)

    mapper_type = db.relationship("Model_RefAttrMapperType", 
        primaryjoin="Model_ConfigProductMapperSet.config_attr_mapper_type_id== Model_RefAttrMapperType.ref_id")

    __mapper_args__ = {
        'polymorphic_on': config_attr_type_code,
        'polymorphic_identity': '__default__'
    }

    @classmethod
    def find_by_product(cls, product_id):
        return cls.query.filter(cls.config_product_id == product_id).all()

class Model_ConfigProductMapperSet_Gender(Model_ConfigProductMapperSet): 
    mappers = db.relationship("Model_ConfigProductMapperDetail", 
        primaryjoin="Model_ConfigProductMapperSet_Gender.config_product_mapper_set_id == Model_ConfigProductMapperDetail.config_product_mapper_set_id")

    __mapper_args__ = {
        'polymorphic_identity': 'gender'
    }


class Model_ConfigProductMapperSet_SmokerStatus(Model_ConfigProductMapperSet): 
    mappers = db.relationship("Model_ConfigProductMapperDetail", 
        primaryjoin="Model_ConfigProductMapperSet_SmokerStatus.config_product_mapper_set_id == Model_ConfigProductMapperDetail.config_product_mapper_set_id")

    __mapper_args__ = {
        'polymorphic_identity': 'smoker_status'
    }
