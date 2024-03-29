import datetime
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.shared import BaseModel
from .Config_Provision import Model_ConfigProvision

from ..tables import TBL_NAMES

CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]
CONFIG_PROVISION_STATE = TBL_NAMES["CONFIG_PROVISION_STATE"]
CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]


class Model_ConfigProvisionState(BaseModel):
    __tablename__ = CONFIG_PROVISION_STATE
    __table_args__ = (
        db.UniqueConstraint(
            "config_provision_id",
            "state_id",
            "config_provision_state_effective_date",
        ),
        db.CheckConstraint(
            "config_provision_state_effective_date <= config_provision_state_expiration_date"
        ),
    )

    config_provision_state_id = db.Column(db.Integer, primary_key=True)
    config_provision_id = db.Column(
        db.ForeignKey(f"{CONFIG_PROVISION}.config_provision_id"), nullable=False
    )
    state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"), nullable=False)

    config_provision_state_effective_date = db.Column(db.Date, nullable=False)
    config_provision_state_expiration_date = db.Column(db.Date, nullable=False)

    parent = db.relationship("Model_ConfigProvision")
    state = db.relationship("Model_RefStates")

    @classmethod
    def get_provision_states_by_product(
        cls, product_id: int, state_id: int, effective_date: datetime.date
    ):
        return (
            db.session.query(cls)
            .join(
                Model_ConfigProvision,
                Model_ConfigProvision.config_provision_id == cls.config_provision_id,
            )
            .filter(
                Model_ConfigProvision.config_product_id == product_id,
                cls.state_id == state_id,
                cls.config_provision_state_effective_date <= effective_date,
                cls.config_provision_state_expiration_date >= effective_date,
            )
            .options(joinedload(cls.parent))
            .all()
        )
