from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_FACTOR = TBL_NAMES["CONFIG_FACTOR"]
CONFIG_PROVISION = TBL_NAMES["CONFIG_PROVISION"]
SELECTION_FACTOR = TBL_NAMES["SELECTION_FACTOR"]
SELECTION_PLAN = TBL_NAMES["SELECTION_PLAN"]
SELECTION_PROVISION = TBL_NAMES["SELECTION_PROVISION"]


class Model_SelectionFactor(BaseModel):
    __tablename__ = SELECTION_FACTOR

    selection_factor_id = db.Column(db.Integer, primary_key=True)
    selection_provision_id = db.Column(
        db.ForeignKey(
            f"{SELECTION_PROVISION}.selection_provision_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
    )
    config_factor_id = db.Column(
        db.ForeignKey(
            f"{CONFIG_FACTOR}.config_factor_id",
            ondelete="SET NULL",
            onupdate="SET NULL",
        ),
        nullable=True,
    )
    selection_rate_table_age_value = db.Column(db.Integer, default=-1)
    selection_rating_attr_id1 = db.Column(db.Integer, default=-1)
    selection_rating_attr_id2 = db.Column(db.Integer, default=-1)
    selection_rating_attr_id3 = db.Column(db.Integer, default=-1)
    selection_rating_attr_id4 = db.Column(db.Integer, default=-1)
    selection_rating_attr_id5 = db.Column(db.Integer, default=-1)
    selection_rating_attr_id6 = db.Column(db.Integer, default=-1)
    selection_factor_value = db.Column(db.Numeric(8, 5), default=1)
