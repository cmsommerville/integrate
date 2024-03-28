from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from .Config_Provision import Model_ConfigProvision
from .Config_ProvisionState import Model_ConfigProvisionState

from ..tables import TBL_NAMES

CONFIG_FACTOR_SET = TBL_NAMES["CONFIG_FACTOR_SET"]
CONFIG_PROVISION_STATE = TBL_NAMES["CONFIG_PROVISION_STATE"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_PROVISION = TBL_NAMES["SELECTION_PROVISION"]


class Model_SelectionProvision(BaseModel):
    __tablename__ = SELECTION_PROVISION
    __table_args__ = (
        db.UniqueConstraint("selection_plan_id", "config_provision_state_id"),
    )

    selection_provision_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    config_provision_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PROVISION_STATE}.config_provision_state_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    selection_value = db.Column(db.String(100), nullable=True)

    @hybrid_property
    def config_provision(self):
        return (
            db.session.query(Model_ConfigProvision)
            .join(
                Model_ConfigProvisionState,
                Model_ConfigProvisionState.config_provision_id
                == Model_ConfigProvision.config_provision_id,
            )
            .filter(
                Model_ConfigProvisionState.config_provision_state_id
                == self.config_provision_state_id
            )
            .first()
        )

    parent = db.relationship("Model_SelectionPlan")
    config_provision_state = db.relationship("Model_ConfigProvisionState")
    factors = db.relationship("Model_SelectionFactor")

    @classmethod
    def find_by_plan(cls, selection_plan_id: int):
        return cls.query.filter(cls.selection_plan_id == selection_plan_id)
