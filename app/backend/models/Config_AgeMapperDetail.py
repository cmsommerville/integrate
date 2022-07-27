from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_MAPPER_DETAIL = TBL_NAMES['CONFIG_AGE_MAPPER_DETAIL']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']

class Model_ConfigAgeMapperDetail(BaseModel):
    __tablename__ = CONFIG_AGE_MAPPER_DETAIL
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'from_age_value'),
    )

    config_age_mapper_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id", onupdate="CASCADE", ondelete="CASCADE"))
    from_age_value = db.Column(db.Integer, nullable=False)
    to_age_value = db.Column(db.Integer, nullable=False)
    
