from flask import request
from sqlalchemy import event
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.extensions import db


@event.listens_for(db.session, 'after_begin')
def set_db_user_id(session, transaction, connection, *args, **kwargs):
    try: 
        header, data = verify_jwt_in_request()
        identity = get_jwt_identity()
        roles = ';'.join(identity.get('roles', []))
        stmt = f"EXEC sp_set_session_context 'user_roles', N'{roles}'"
        connection.execute(stmt)
    except: 
        pass