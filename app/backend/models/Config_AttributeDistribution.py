from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DISTRIBUTION = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION']
CONFIG_ATTRIBUTE_DISTRIBUTION_SET = TBL_NAMES['CONFIG_ATTRIBUTE_DISTRIBUTION_SET']
CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']

class Model_ConfigAttributeDistribution(BaseModel):
    __tablename__ = CONFIG_ATTRIBUTE_DISTRIBUTION
    __table_args__ = (
        db.UniqueConstraint('config_attr_distribution_set_id', 'config_attr_detail_id'),
    )

    config_attr_distribution_id = db.Column(db.Integer, primary_key=True)
    config_attr_distribution_set_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DISTRIBUTION_SET}.config_attr_distribution_set_id", onupdate="CASCADE", ondelete="CASCADE"))
    config_attr_detail_id = db.Column(db.ForeignKey(f"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"))
    weight = db.Column(db.Numeric(12,5), nullable=False)
