from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES["CONFIG_ATTRIBUTE_DETAIL"]

CONFIG_RATING_MAPPER_DETAIL = TBL_NAMES["CONFIG_RATING_MAPPER_DETAIL"]
CONFIG_RATING_MAPPER_SET = TBL_NAMES["CONFIG_RATING_MAPPER_SET"]


class Model_ConfigRatingMapperDetail(BaseModel):
    __tablename__ = CONFIG_RATING_MAPPER_DETAIL

    config_rating_mapper_detail_id = db.Column(db.Integer, primary_key=True)
    config_rating_mapper_set_id = db.Column(
        db.ForeignKey(f"{CONFIG_RATING_MAPPER_SET}.config_rating_mapper_set_id")
    )
    rate_table_attribute_detail_id = db.Column(
        db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id")
    )
    output_attribute_detail_id = db.Column(
        db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id")
    )
    weight = db.Column(db.Numeric(8, 5), default=False)
