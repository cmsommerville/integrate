from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_BENEFIT = TBL_NAMES["CONFIG_BENEFIT"]
CONFIG_PLAN_DESIGN_DETAIL = TBL_NAMES["CONFIG_PLAN_DESIGN_DETAIL"]
CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]


class Model_ConfigPlanDesignDetail(BaseModel):
    __tablename__ = CONFIG_PLAN_DESIGN_DETAIL
    __table_args__ = (
        db.UniqueConstraint(
            "config_plan_design_set_id", "config_parent_type_code", "config_parent_id"
        ),
    )

    config_plan_design_detail_id = db.Column(db.Integer, primary_key=True)
    config_plan_design_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PLAN_DESIGN_SET}.config_plan_design_set_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    config_parent_type_code = db.Column(db.String(50), nullable=False)
    config_parent_id = db.Column(db.Integer, nullable=False)
    default_value = db.Column(db.Numeric(12, 2), nullable=True)

    __mapper_args__ = {
        "polymorphic_on": config_parent_type_code,
        "polymorphic_identity": "base",
    }


class Model_ConfigPlanDesignDetail_Benefit(Model_ConfigPlanDesignDetail):
    __mapper_args__ = {"polymorphic_identity": "benefit"}
    benefit = db.relationship(
        "Model_ConfigBenefit",
        primaryjoin="Model_ConfigPlanDesignDetail_Benefit.config_parent_id == Model_ConfigBenefit.config_benefit_id",
        foreign_keys="Model_ConfigBenefit.config_benefit_id",
        uselist=False,
        lazy="joined",
    )


class Model_ConfigPlanDesignDetail_PlanDesign(Model_ConfigPlanDesignDetail):
    __mapper_args__ = {"polymorphic_identity": "plan_design"}
    plan_design_set = db.relationship(
        "Model_ConfigPlanDesignSet",
        primaryjoin="Model_ConfigPlanDesignDetail_PlanDesign.config_parent_id == Model_ConfigPlanDesignSet.config_plan_design_set_id",
        foreign_keys="Model_ConfigPlanDesignSet.config_plan_design_set_id",
        uselist=False,
        lazy="joined",
    )
