from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_RELATIONSHIP_MAPPER_SET = TBL_NAMES['CONFIG_RELATIONSHIP_MAPPER_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']


class Model_ConfigRelationshipMapperSet(BaseModel):
    __tablename__ = CONFIG_RELATIONSHIP_MAPPER_SET
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'config_relationship_mapper_set_code'),
    )

    config_relationship_mapper_set_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f'{CONFIG_PRODUCT}.config_product_id'), nullable=False)
    config_relationship_mapper_set_code = db.Column(db.String(30), nullable=False)
    config_relationship_mapper_set_label = db.Column(db.String(100), nullable=False, 
        comment="Specifies the relationship mapper name")
    is_default =  db.Column(db.Boolean, nullable=False)