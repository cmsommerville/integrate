from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_SET = TBL_NAMES["CONFIG_ATTRIBUTE_SET"]


class Model_ConfigAttributeSet(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_SET

    config_attr_set_id = db.Column(db.Integer, primary_key=True)
    config_attr_set_code = db.Column(db.String(30), nullable=False)
    config_attr_set_label = db.Column(db.String(100))

    attributes = db.relationship(
        "Model_ConfigAttributeDetail",
        primaryjoin="Model_ConfigAttributeSet.config_attr_set_id == Model_ConfigAttributeDetail.config_attr_set_id",
        backref="parent",
        passive_deletes=True,
    )
