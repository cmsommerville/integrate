from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_RATING_MAPPER_COLLECTION = TBL_NAMES["CONFIG_RATING_MAPPER_COLLECTION"]
CONFIG_RATING_MAPPER_SET = TBL_NAMES["CONFIG_RATING_MAPPER_SET"]


class Model_ConfigRatingMapperSet(BaseModel):
    __tablename__ = CONFIG_RATING_MAPPER_SET

    config_rating_mapper_set_id = db.Column(db.Integer, primary_key=True)
    config_rating_mapper_set_label = db.Column(db.String(255), nullable=False)
    config_rating_mapper_collection_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_RATING_MAPPER_COLLECTION}.config_rating_mapper_collection_id"
        )
    )
    is_composite = db.Column(db.Boolean, default=False)
    is_employer_paid = db.Column(db.Boolean, default=False)
