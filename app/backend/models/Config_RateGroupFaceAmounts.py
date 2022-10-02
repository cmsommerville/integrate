from app.backend.models.Config_AttributeDetail import CONFIG_ATTRIBUTE_DETAIL
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
CONFIG_RATE_GROUP_FACE_AMOUNTS = TBL_NAMES['CONFIG_RATE_GROUP_FACE_AMOUNTS']

class Model_ConfigRateGroupFaceAmounts(BaseModel):
    __tablename__ = CONFIG_RATE_GROUP_FACE_AMOUNTS
    __table_args__ = (
        db.UniqueConstraint('config_rate_group_id', 
        'config_gender_detail_id', 'config_smoker_status_detail_id', 
        'config_relationship_detail_id', 'face_amount_value'), 
    )

    config_rate_group_face_amount_id = db.Column(db.Integer, primary_key=True)
    config_rate_group_id = db.Column(db.ForeignKey(F"{CONFIG_RATE_GROUP}.config_rate_group_id"), nullable=False)
    config_gender_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_smoker_status_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_relationship_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    face_amount_value = db.Column(db.Numeric(10, 2), nullable=False)