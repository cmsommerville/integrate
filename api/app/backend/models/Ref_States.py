from app.extensions import db
from app.shared import BaseModel
from sqlalchemy import VARCHAR

from ..tables import TBL_NAMES

REF_STATES = TBL_NAMES["REF_STATES"]


class Model_RefStates(BaseModel):
    __tablename__ = REF_STATES
    __table_args__ = (db.UniqueConstraint("state_code"),)

    state_id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(2), nullable=False)
    state_name = db.Column(db.String(100), nullable=False)
    svg_path = db.Column(VARCHAR(None))
