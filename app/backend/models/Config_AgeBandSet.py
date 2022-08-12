from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_BAND_SET = TBL_NAMES['CONFIG_AGE_BAND_SET']

class Model_ConfigAgeBandSet(BaseModel):
    __tablename__ = CONFIG_AGE_BAND_SET

    config_age_band_set_id = db.Column(db.Integer, primary_key = True)
    config_age_band_set_label = db.Column(db.String(100), nullable=False)

    age_bands = db.relationship('Model_ConfigAgeBandDetail')