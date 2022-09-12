from typing import Tuple
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION
    __table_args__ = (
        db.UniqueConstraint('config_provision_version_code'),
    )

    config_provision_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(
        f"{CONFIG_PRODUCT}.config_product_id"), nullable=False)
    ref_provision_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    config_provision_version_code  = db.Column(db.String(30), nullable=False)
    config_provision_type_code = db.Column(db.String(30), nullable=False)
    config_provision_data_type_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"), nullable=False)
    config_provision_description = db.Column(db.String(1000))

    ui_component = db.relationship("Model_ConfigProvisionUI")
    ref_provision = db.relationship("Model_RefProvision",
        primaryjoin="Model_ConfigProvision.ref_provision_id == Model_RefProvision.ref_id")
    data_type = db.relationship("Model_RefDataTypes", lazy='joined', 
        primaryjoin="Model_ConfigProvision.config_provision_data_type_id == Model_RefDataTypes.ref_id")

    __mapper_args__ = {
        'polymorphic_on': config_provision_type_code,
        'polymorphic_identity': '__default__'
    }


class Model_ConfigProvision_Product(Model_ConfigProvision):
    __mapper_args__ = {
        'polymorphic_identity': 'product'
    }

    factors = db.relationship("Model_ConfigFactor")


class Model_ConfigProvision_RateTable(Model_ConfigProvision):
    __mapper_args__ = {
        'polymorphic_identity': 'rate_table'
    }

    factors = db.relationship("Model_ConfigFactor")