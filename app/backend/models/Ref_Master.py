from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

REF_MASTER = TBL_NAMES['REF_MASTER']

class Model_RefMaster(BaseModel):
    __tablename__ = REF_MASTER
    __table_args__ = (
        db.UniqueConstraint('ref_entity_code', 'ref_attr_code',),
    )

    ref_id = db.Column(db.Integer, primary_key=True)
    ref_entity_code = db.Column(db.String(30), nullable=False)
    ref_attr_code = db.Column(db.String(30), nullable=False)
    ref_attr_label = db.Column(db.String(100), nullable=False)
    ref_attr_description = db.Column(db.String(1000))
    ref_attr_symbol = db.Column(db.String(30))
    ref_attr_value = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_on': ref_entity_code,
        'polymorphic_identity': 'ref_master'
    }


class Model_RefAttrMapperType(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'attr_type_code'
    }

class Model_RefBenefit(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'benefit'
    }

class Model_RefCensusStrategy(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'census_strategy'
    }

class Model_RefComparisonOperator(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'comparison_operator'
    }

class Model_RefComponentTypes(Model_RefMaster):

    __mapper_args__ = {
        'polymorphic_identity': 'component_type'
    }

class Model_RefDataTypes(Model_RefMaster):

    __mapper_args__ = {
        'polymorphic_identity': 'data_type'
    }

class Model_RefFactorType(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'factor_type'
    }

class Model_RefInputTypes(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'input_type'
    }

class Model_RefOptionality(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'optionality'
    }

class Model_RefPremiumFrequency(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'premium_frequency'
    }

class Model_RefProductVariation(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'product_variation'
    }

class Model_RefProvision(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'provision'
    }

class Model_RefRatingStrategy(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'rating_strategy'
    }

class Model_RefUnitCode(Model_RefMaster):
    __mapper_args__ = {
        'polymorphic_identity': 'unit_code'
    }

