from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_COVERAGE = TBL_NAMES["CONFIG_COVERAGE"]
CONFIG_PLAN_DESIGN_SET = TBL_NAMES["CONFIG_PLAN_DESIGN_SET"]
SELECTION_COVERAGE = TBL_NAMES["SELECTION_COVERAGE"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionCoverage(BaseModel):
    __tablename__ = SELECTION_COVERAGE
    __table_args__ = (db.UniqueConstraint("selection_plan_id", "config_coverage_id"),)

    selection_coverage_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    config_coverage_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_COVERAGE}.config_coverage_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    config_plan_design_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_PLAN_DESIGN_SET}.config_plan_design_set_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )

    parent = db.relationship("Model_SelectionPlan")
    coverage = db.relationship("Model_ConfigCoverage")
    benefits = db.relationship("Model_SelectionBenefit", back_populates="coverage")
    plan_design = db.relationship("Model_ConfigPlanDesignSet")

    @classmethod
    def find_by_plan(cls, selection_plan_id: int):
        return cls.query.filter(cls.selection_plan_id == selection_plan_id).all()
