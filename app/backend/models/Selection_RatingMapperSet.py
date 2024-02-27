from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_RATING_MAPPER_SET = TBL_NAMES["CONFIG_RATING_MAPPER_SET"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_RATING_MAPPER_SET = TBL_NAMES["SELECTION_RATING_MAPPER_SET"]


class Model_SelectionRatingMapperSet(BaseModel):
    __tablename__ = SELECTION_RATING_MAPPER_SET
    __table_args__ = (
        db.UniqueConstraint("selection_plan_id", "selection_rating_mapper_set_type"),
        db.CheckConstraint(
            "selection_rating_mapper_set_type IN ('selection_rating_mapper_set_id1', 'selection_rating_mapper_set_id2', 'selection_rating_mapper_set_id3', 'selection_rating_mapper_set_id4', 'selection_rating_mapper_set_id5', 'selection_rating_mapper_set_id6')"
        ),
    )

    selection_rating_mapper_set_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PLAN}.selection_plan_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    selection_rating_mapper_set_type = db.Column(db.String(50))
    config_rating_mapper_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )
    has_custom_weights = db.Column(db.Boolean, default=False)

    mapper_details = db.relationship("Model_SelectionRatingMapperDetail", lazy="joined")
