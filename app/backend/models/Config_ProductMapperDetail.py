from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_PRODUCT_MAPPER_DETAIL = TBL_NAMES['CONFIG_PRODUCT_MAPPER_DETAIL']
CONFIG_PRODUCT_MAPPER_SET = TBL_NAMES['CONFIG_PRODUCT_MAPPER_SET']

class Model_ConfigProductMapperDetail(BaseModel):
    __tablename__ = CONFIG_PRODUCT_MAPPER_DETAIL
    __table_args__ = (
        db.UniqueConstraint('config_product_mapper_set_id', 'from_config_attr_detail_id'),
    )

    config_product_mapper_detail_id = db.Column(db.Integer, primary_key=True)
    config_product_mapper_set_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT_MAPPER_SET}.config_product_mapper_set_id", onupdate="CASCADE", ondelete="CASCADE"))
    from_config_attr_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"))
    to_config_attr_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"))
    
