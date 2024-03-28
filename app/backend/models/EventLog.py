from app.extensions import db
from app.auth import get_user
from sqlalchemy import text
from sqlalchemy.dialects.mssql import NVARCHAR

from ..tables import TBL_NAMES

EVENT_LOG = TBL_NAMES["EVENT_LOG"]


class Model_EventLog(db.Model):
    __tablename__ = EVENT_LOG

    event_id = db.Column(db.Integer, primary_key=True)
    event_type_code = db.Column(db.String(100), nullable=False)
    event_payload = db.Column(NVARCHAR(None), nullable=True)

    created_dts = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_dts = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    updated_by = db.Column(
        db.String(50),
        default=lambda x: get_user().get("user_name", "UNKNOWN"),
        onupdate=lambda x: get_user().get("user_name", "UNKNOWN"),
    )
