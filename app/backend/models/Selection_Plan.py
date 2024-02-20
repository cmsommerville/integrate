from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT = TBL_NAMES["CONFIG_PRODUCT"]
CONFIG_PRODUCT_VARIATION = TBL_NAMES["CONFIG_PRODUCT_VARIATION"]
CONFIG_RATING_MAPPER_SET = TBL_NAMES["CONFIG_RATING_MAPPER_SET"]
REF_MASTER = TBL_NAMES["REF_MASTER"]
REF_STATES = TBL_NAMES["REF_STATES"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_PLAN_ACL = TBL_NAMES["SELECTION_PLAN_ACL"]


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
    config_product_variation_id = db.Column(
        db.ForeignKey(f"{CONFIG_PRODUCT_VARIATION}.config_product_variation_id")
    )
    cloned_from_selection_plan_id = db.Column(
        db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=True
    )
    is_template = db.Column(db.Boolean, default=False)
    plan_status = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))

    selection_rating_mapper_set_id1 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )
    selection_rating_mapper_set_id2 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )
    selection_rating_mapper_set_id3 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )
    selection_rating_mapper_set_id4 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )
    selection_rating_mapper_set_id5 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )
    selection_rating_mapper_set_id6 = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id"),
        nullable=True,
    )

    rating_mapper_set1 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id1 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
    rating_mapper_set2 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id2 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
    rating_mapper_set3 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id3 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
    rating_mapper_set4 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id4 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
    rating_mapper_set5 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id5 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
    rating_mapper_set6 = db.relationship(
        "Model_ConfigRatingMapperSet",
        primaryjoin="Model_SelectionPlan.selection_rating_mapper_set_id6 == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )

    situs_state = db.relationship("Model_RefStates")
    acl = db.relationship("Model_SelectionPlan_ACL")
