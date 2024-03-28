from app.extensions import db
from app.shared import BaseModel
from app.shared.utils import system_temporal_hint
from sqlalchemy.ext.hybrid import hybrid_method

from ..tables import TBL_NAMES
from .Selection_BenefitDuration import Model_SelectionBenefitDuration

CONFIG_BENEFIT_VARIATION_STATE = TBL_NAMES["CONFIG_BENEFIT_VARIATION_STATE"]
SELECTION_BENEFIT = TBL_NAMES["SELECTION_BENEFIT"]
SELECTION_COVERAGE = TBL_NAMES["SELECTION_COVERAGE"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]


class Model_SelectionBenefit(BaseModel):
    __tablename__ = SELECTION_BENEFIT
    __table_args__ = (
        db.UniqueConstraint("selection_plan_id", "config_benefit_variation_state_id"),
    )

    selection_benefit_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
        ),
        index=True,
    )
    selection_coverage_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_COVERAGE}.selection_coverage_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
    )
    config_benefit_variation_state_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_BENEFIT_VARIATION_STATE}.config_benefit_variation_state_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        nullable=False,
    )
    selection_value = db.Column(db.Numeric(12, 2), nullable=False)

    parent = db.relationship(
        "Model_SelectionPlan",
        cascade="all, delete",
    )
    coverage = db.relationship("Model_SelectionCoverage", back_populates="benefits")
    config_benefit_variation_state = db.relationship(
        "Model_ConfigBenefitVariationState"
    )
    duration_sets = db.relationship("Model_SelectionBenefitDuration")

    @hybrid_method
    def get_benefit_durations(self, t=None, *args, **kwargs):
        """
        This method returns the benefit duration list for the selection plan.
        If `t` is provided, it will return the benefit duration list as of that time using system-temporal table queries.
        """
        hint = system_temporal_hint(t)
        return (
            db.session.query(Model_SelectionBenefitDuration)
            .with_hint(Model_SelectionBenefitDuration, hint)
            .filter_by(selection_benefit_id=self.selection_benefit_id)
            .all()
        )

    @classmethod
    def find_by_plan(cls, selection_plan_id: int):
        return cls.query.filter(cls.selection_plan_id == selection_plan_id).all()
