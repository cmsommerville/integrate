from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_PRODUCT_STATE = TBL_NAMES['CONFIG_PRODUCT_STATE']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
REF_STATES = TBL_NAMES['REF_STATES']


class Model_ConfigProductState(BaseModel):
    __tablename__ = CONFIG_PRODUCT_STATE
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'state_id'),
        db.CheckConstraint('config_product_state_effective_date <= config_product_state_expiration_date')
    )

    config_product_state_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"))
    state_id = db.Column(db.ForeignKey(f"{REF_STATES}.state_id"))
    config_product_state_effective_date = db.Column(db.Date, nullable=False)
    config_product_state_expiration_date = db.Column(db.Date, nullable=False)

    state = db.relationship("Model_RefStates")

    @classmethod
    def find_by_product(cls, id):
        return cls.query.filter(cls.config_product_id == id).all()


