from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_AGE_BAND_DETAIL = TBL_NAMES['CONFIG_AGE_BAND_DETAIL']
CONFIG_AGE_BAND_SET = TBL_NAMES['CONFIG_AGE_BAND_SET']

class Model_ConfigAgeBandDetail(BaseModel):
    __tablename__ = CONFIG_AGE_BAND_DETAIL
    __table_args__ = (
        db.UniqueConstraint('config_age_band_set_id', 'age_band_lower'),
        db.CheckConstraint('age_band_lower <= age_band_upper')
    )

    config_age_band_detail_id = db.Column(db.Integer, primary_key=True)
    config_age_band_set_id = db.Column(db.ForeignKey(f"{CONFIG_AGE_BAND_SET}.config_age_band_set_id"))
    age_band_lower = db.Column(db.Integer, nullable=False)
    age_band_upper = db.Column(db.Integer, nullable=False)
