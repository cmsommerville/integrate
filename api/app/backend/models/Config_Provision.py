from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_DROPDOWN_SET = TBL_NAMES["CONFIG_DROPDOWN_SET"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigProvision(BaseModel):
    __tablename__ = CONFIG_PROVISION
    __table_args__ = (
        db.UniqueConstraint("config_product_id", "config_provision_code"),
    )

    config_provision_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(
        db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), nullable=False
    )
    config_provision_code = db.Column(db.String(30), nullable=False)
    config_provision_label = db.Column(db.String(100), nullable=False)
    config_provision_data_type_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id"), nullable=False
    )
    config_dropdown_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_DROPDOWN_SET}.config_dropdown_set_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )
    config_provision_description = db.Column(db.String(1000))
    default_value = db.Column(db.String(100), nullable=True)
    is_default_related_attribute = db.Column(db.Boolean, default=False)

    parent = db.relationship("Model_ConfigProduct")
    dropdown_set = db.relationship("Model_ConfigDropdownSet")
    data_type = db.relationship(
        "Model_RefDataTypes",
        lazy="joined",
        primaryjoin="Model_ConfigProvision.config_provision_data_type_id == Model_RefDataTypes.ref_id",
    )
    factors = db.relationship(
        "Model_ConfigFactorSet", order_by="Model_ConfigFactorSet.factor_priority"
    )

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.config_product_id == id).all()
