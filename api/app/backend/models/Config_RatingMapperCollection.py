from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_RATING_MAPPER_COLLECTION = TBL_NAMES["CONFIG_RATING_MAPPER_COLLECTION"]
CONFIG_RATING_MAPPER_SET = TBL_NAMES["CONFIG_RATING_MAPPER_SET"]
CONFIG_ATTRIBUTE_SET = TBL_NAMES["CONFIG_ATTRIBUTE_SET"]
REF_MASTER = TBL_NAMES["REF_MASTER"]


class Model_ConfigRatingMapperCollection(BaseModel):
    __tablename__ = CONFIG_RATING_MAPPER_COLLECTION

    config_rating_mapper_collection_id = db.Column(db.Integer, primary_key=True)
    config_attribute_set_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_ATTRIBUTE_SET}.config_attr_set_id", ondelete="NO ACTION"
        )
    )
    config_rating_mapper_collection_label = db.Column(db.String(100))
    rating_strategy_id = db.Column(
        db.ForeignKey(f"{REF_MASTER}.ref_id", ondelete="NO ACTION")
    )
    default_config_rating_mapper_set_id = db.Column(db.Integer, nullable=True)
    is_selectable = db.Column(db.Boolean, default=False)
    can_override_distribution = db.Column(db.Boolean, default=False)

    attribute_set = db.relationship("Model_ConfigAttributeSet")
    mapper_sets = db.relationship("Model_ConfigRatingMapperSet")
    rating_strategy = db.relationship("Model_RefRatingStrategy")
    default_mapper_set = db.relationship(
        "Model_ConfigRatingMapperSet",
        foreign_keys=[default_config_rating_mapper_set_id],
        primaryjoin="Model_ConfigRatingMapperCollection.default_config_rating_mapper_set_id == Model_ConfigRatingMapperSet.config_rating_mapper_set_id",
    )
