from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.extensions import db

def app_set_superuser():
    def wrapper(fn): 
        @wraps(fn)
        def decorator(*args, **kwargs): 
            db.session.execute(f"EXEC sp_set_session_context 'user_id', -99")
            return fn(*args, **kwargs)
        return decorator 
    return wrapper


def app_auth_required(): 
    def wrapper(fn): 
        @wraps(fn)
        def decorator(*args, **kwargs): 
            verify_jwt_in_request()
            identity = get_jwt_identity()
            db.session.execute(f"EXEC sp_set_session_context 'user_id', {identity.get('user_id')}")
            return fn(*args, **kwargs)
        return decorator 
    return wrapper

