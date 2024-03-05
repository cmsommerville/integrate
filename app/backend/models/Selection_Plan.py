from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PRODUCT_VARIATION_STATE = TBL_NAMES["CONFIG_PRODUCT_VARIATION_STATE"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_PLAN_ACL = TBL_NAMES["SELECTION_PLAN_ACL"]
SELECTION_RATING_MAPPER_SET = TBL_NAMES["SELECTION_RATING_MAPPER_SET"]


class Model_SelectionPlan_ACL(BaseModel):
    __tablename__ = SELECTION_PLAN_ACL
    __table_args__ = (
        db.CheckConstraint("NOT (user_name IS NULL AND role_name IS NULL)"),
    )

    selection_plan_acl_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    user_name = db.Column(db.String(100), nullable=True)
    role_name = db.Column(db.String(100), nullable=True)
    with_grant_option = db.Column(db.Boolean, default=False)


class Model_SelectionPlan(BaseModel):
    __tablename__ = SELECTION_PLAN

    selection_plan_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"))
    selection_plan_effective_date = db.Column(db.Date, nullable=False)
    situs_state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"))
    config_product_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PRODUCT_VARIATION_STATE}.config_product_variation_state_id"
        )
    )
    selection_group_id = db.Column(db.Integer, nullable=True)
    cloned_from_selection_plan_id = db.Column(
        db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=True
    )
    is_template = db.Column(db.Boolean, default=False)
    plan_status = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))

    situs_state = db.relationship("Model_RefStates")
    config_product = db.relationship("Model_ConfigProduct")
    config_product_variation_state = db.relationship(
        "Model_ConfigProductVariationState"
    )
    acl = db.relationship("Model_SelectionPlan_ACL")
    rating_mapper_sets = db.relationship("Model_SelectionRatingMapperSet")
