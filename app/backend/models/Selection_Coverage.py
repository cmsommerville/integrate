from app.extensions import db
from app.shared import BaseModel
from app.shared.utils import system_temporal_hint
from sqlalchemy.ext.hybrid import hybrid_method

from ..tables import TBL_NAMES
from .Selection_Benefit import Model_SelectionBenefit

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

    @hybrid_method
    def get_benefits(self, t=None, *args, **kwargs):
        """
        This method returns the benefit list for the selection plan.
        If `t` is provided, it will return the benefit list as of that time using system-temporal table queries.
        """
        hint = system_temporal_hint(t)
        return (
            db.session.query(Model_SelectionBenefit)
            .with_hint(Model_SelectionBenefit, hint)
            .filter_by(selection_coverage_id=self.selection_coverage_id)
            .all()
        )

    parent = db.relationship("Model_SelectionPlan")
    coverage = db.relationship("Model_ConfigCoverage")
    benefits = db.relationship("Model_SelectionBenefit", back_populates="coverage")
    plan_design = db.relationship("Model_ConfigPlanDesignSet")

    @classmethod
    def find_by_plan(cls, selection_plan_id: int):
        return cls.query.filter(cls.selection_plan_id == selection_plan_id).all()
