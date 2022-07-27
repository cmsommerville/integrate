from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_RELATIONSHIP_MAPPER_DETAIL = TBL_NAMES['CONFIG_RELATIONSHIP_MAPPER_DETAIL']
CONFIG_RELATIONSHIP_MAPPER_SET = TBL_NAMES['CONFIG_RELATIONSHIP_MAPPER_SET']

class Model_ConfigRelationshipMapperDetail(BaseModel):
    __tablename__ = CONFIG_RELATIONSHIP_MAPPER_DETAIL
    __table_args__ = (
        db.UniqueConstraint('config_relationship_mapper_set_id', 'from_config_attr_detail_id', 'to_config_attr_detail_id'),
    )

    config_relationship_mapper_detail_id = db.Column(db.Integer, primary_key=True)
    config_relationship_mapper_set_id = db.Column(db.ForeignKey(f"{CONFIG_RELATIONSHIP_MAPPER_SET}.config_relationship_mapper_set_id", onupdate="CASCADE", ondelete="CASCADE"))
    from_config_attr_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"))
    to_config_attr_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"))
    
    from_relationship = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigRelationshipMapperDetail.from_config_attr_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")
    to_relationship = db.relationship("Model_ConfigAttributeDetail", 
        primaryjoin="Model_ConfigRelationshipMapperDetail.to_config_attr_detail_id == Model_ConfigAttributeDetail.config_attr_detail_id")