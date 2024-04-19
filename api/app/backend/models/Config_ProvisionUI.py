from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]
CONFIG_PROVISION_UI = TBL_NAMES["CONFIG_PROVISION_UI"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigProvisionUI(BaseModel):
    __tablename__ = CONFIG_PROVISION_UI
    __table_args__ = (db.UniqueConstraint("config_provision_id"),)

    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION}.config_provision_id"), primary_key=True
    )
    component_type_code = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "BASE",
        "polymorphic_on": component_type_code,
    }

    ui_input = db.relationship("Model_ConfigProvisionUI_Input", uselist=False)
    ui_select = db.relationship("Model_ConfigProvisionUI_Select", uselist=False)
    ui_checkbox = db.relationship("Model_ConfigProvisionUI_Checkbox", uselist=False)


class Model_ConfigProvisionUI_Checkbox(Model_ConfigProvisionUI):
    __tablename__ = f"{CONFIG_PROVISION_UI}__checkbox"

    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION_UI}.config_provision_id"), primary_key=True
    )
    is_switch = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        "polymorphic_identity": "CHECKBOX",
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.config_provision_id == id).first()


class Model_ConfigProvisionUI_Input(Model_ConfigProvisionUI):
    __tablename__ = f"{CONFIG_PROVISION_UI}__input"

    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION_UI}.config_provision_id"), primary_key=True
    )
    input_type_id = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    step_value = db.Column(db.Float)
    min_length = db.Column(db.Integer)
    max_length = db.Column(db.Integer)
    placeholder = db.Column(db.String(100))

    input_type = db.relationship(
        "Model_RefInputTypes",
        primaryjoin="Model_ConfigProvisionUI_Input.input_type_id == Model_RefInputTypes.ref_id",
    )

    __mapper_args__ = {
        "polymorphic_identity": "INPUT",
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.config_provision_id == id).first()


class Model_ConfigProvisionUI_Select(Model_ConfigProvisionUI):
    __tablename__ = f"{CONFIG_PROVISION_UI}__select"

    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION_UI}.config_provision_id"), primary_key=True
    )
    is_radio = db.Column(db.Boolean, default=False)
    default_config_provision_ui_select_item_id = db.Column(db.Integer, nullable=True)

    items = db.relationship("Model_ConfigProvisionUI_SelectItem")
    default_item = db.relationship(
        "Model_ConfigProvisionUI_SelectItem",
        foreign_keys=[default_config_provision_ui_select_item_id],
        primaryjoin="Model_ConfigProvisionUI_Select.default_config_provision_ui_select_item_id == Model_ConfigProvisionUI_SelectItem.config_provision_ui_select_item_id",
    )

    __mapper_args__ = {
        "polymorphic_identity": "SELECT",
    }

    @classmethod
    def find_one(cls, id: int):
        return cls.query.filter(cls.config_provision_id == id).first()


class Model_ConfigProvisionUI_SelectItem(BaseModel):
    __tablename__ = f"{CONFIG_PROVISION_UI}__select_items"

    config_provision_ui_select_item_id = db.Column(db.Integer, primary_key=True)
    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION_UI}.config_provision_id")
    )
    item_code = db.Column(db.String(30))
    item_label = db.Column(db.String(100))
