from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from sqlalchemy import event
from app.extensions import db


@event.listens_for(db.session, 'after_begin')
def set_db_user_id(session, transaction, connection, *args, **kwargs):
    try: 
        verify_jwt_in_request()
        identity = get_jwt_identity()
        user_id = identity.get('user_id', 0)
        stmt = f"EXEC sp_set_session_context 'user_id', {user_id}"
        connection.execute(stmt)
    except: 
        pass