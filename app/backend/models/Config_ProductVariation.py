from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_BAND_SET = TBL_NAMES['CONFIG_AGE_BAND_SET']
CONFIG_PRODUCT = TBL_NAMES['CONFIG_PRODUCT']
CONFIG_PRODUCT_VARIATION = TBL_NAMES['CONFIG_PRODUCT_VARIATION']



class Model_ConfigProductVariation(BaseModel):
    __tablename__ = CONFIG_PRODUCT_VARIATION
    __table_args__ = (
        db.UniqueConstraint('config_product_id', 'config_product_variation_code'),
        db.CheckConstraint('config_product_variation_effective_date <= config_product_variation_expiration_date')
    )

    config_product_variation_id = db.Column(db.Integer, primary_key=True)
    config_product_id = db.Column(db.ForeignKey(f"{CONFIG_PRODUCT}.config_product_id"), index=True)
    config_product_variation_code = db.Column(db.String(30), nullable=False)
    config_product_variation_label = db.Column(db.String(100), nullable=False)
    config_product_variation_effective_date = db.Column(db.Date(), nullable=False)
    config_product_variation_expiration_date = db.Column(db.Date(), nullable=False)
    config_age_band_set_id = db.Column(db.ForeignKey(F"{CONFIG_AGE_BAND_SET}.config_age_band_set_id"))

    age_band_set = db.relationship("Model_ConfigAgeBandSet")

    @classmethod
    def find_by_product(cls, id: int):
        return cls.query.filter(cls.config_product_id == id).all()

