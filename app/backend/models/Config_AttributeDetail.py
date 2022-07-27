from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_ATTRIBUTE_SET = TBL_NAMES['CONFIG_ATTRIBUTE_SET']

class Model_ConfigAttributeDetail(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_DETAIL
    __table_args__ = (
        db.UniqueConstraint('config_attr_set_id', 'config_attr_detail_code'),
    )

    config_attr_detail_id = db.Column(db.Integer, primary_key=True)
    config_attr_set_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_SET}.config_attr_set_id"))
    config_attr_detail_code = db.Column(db.String(30), nullable=False)
    config_attr_detail_label = db.Column(db.String(100))
    is_composite_id = db.Column(db.Boolean, default=False)
