from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_BAND_SET = TBL_NAMES['CONFIG_AGE_BAND_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATION = TBL_NAMES['CONFIG_PRODUCT_VARIATION']
REF_MASTER = TBL_NAMES['REF_MASTER']



class Model_ConfigProductVariation(BaseModel):
    __tablename__ = CONFIG_PRODUCT_VARIATION
    __table_args__ = (
        db.UniqueConstraint('config_product_variation_version_code'),
    )
    
    config_product_variation_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), index=True)
    ref_product_variation_id = db.Column(db.ForeignKey(f"{REF_MASTER}.ref_id"))
    config_product_variation_version_code = db.Column(db.String(30), nullable=False)

    ref_product_variation = db.relationship("Model_RefProductVariation",  
        primaryjoin="Model_ConfigProductVariation.ref_product_variation_id == Model_RefProductVariation.ref_id")

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.config_product_id == id).all()

