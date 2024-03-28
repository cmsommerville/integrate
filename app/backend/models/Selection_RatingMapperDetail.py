from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES["CONFIG_ATTRIBUTE_DETAIL"]
CONFIG_RATING_MAPPER_DETAIL = TBL_NAMES["CONFIG_RATING_MAPPER_DETAIL"]
SELECTION_RATING_MAPPER_DETAIL = TBL_NAMES["SELECTION_RATING_MAPPER_DETAIL"]
SELECTION_RATING_MAPPER_SET = TBL_NAMES["SELECTION_RATING_MAPPER_SET"]


class Model_SelectionRatingMapperDetail(BaseModel):
    __tablename__ = SELECTION_RATING_MAPPER_DETAIL

    selection_rating_mapper_detail_id = db.Column(db.Integer, primary_key=True)
    selection_rating_mapper_set_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_RATING_MAPPER_SET}.selection_rating_mapper_set_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    config_rating_mapper_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_DETAIL}.config_rating_mapper_detail_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )
    rate_table_attribute_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
    )
    output_attribute_detail_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
    )
    default_weight = db.Column(db.Numeric(8, 5), default=1)
    weight = db.Column(db.Numeric(8, 5), default=1)
