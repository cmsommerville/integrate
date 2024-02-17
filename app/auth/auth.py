import functools
from flask import session
from sqlalchemy.sql import text
from datetime import datetime, timezone


def validate_user(user):
    if user.get("auth_user_id") is None:
        raise ValueError("User must have auth_user_id key")
    if user.get("user_name") is None:
        raise ValueError("User must have user_name key")
    if not isinstance(user.get("roles"), list):
        raise ValueError("User must have roles key")
    return {
        "auth_user_id": user.get("auth_user_id"),
        "user_name": user.get("user_name"),
        "roles": user.get("roles"),
        "permissions": user.get("permissions"),
    }


def get_user():
    return session.get("user", "UNKNOWN")


def login_user(user):
    try:
        user_data = validate_user(user)
        session["user"] = {
            **user_data,
            "is_authenticated": True,
            "timestamp": datetime.now(timezone.utc).timestamp() * 1000,
        }
    except Exception:
        session["user"] = None


def logout():
    session["user"] = None


def is_authenticated(**kwargs):
    return session.get("user", {}).get("is_authenticated", False)


def get_permissions(**kwargs):
    return session.get("user", {}).get("permissions", [])


def get_user_roles(**kwargs):
    return session.get("user", {}).get("roles", [])


def login_required(**kw):
    def outer(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if is_authenticated():
                return func(*args, **kwargs)
            return {"status": "error", "msg": "User is not authenticated"}, 401

        return wrapper_decorator

    return outer


def authorization_required(func):
    @functools.wraps(func)
    def wrapper_decorator(cls, *args, **kwargs):
        try:
            if cls.permissions.get(func.__name__, None) is None:
                return {
                    "status": "error",
                    "msg": f"Permissions for method `{func.__name__}` not defined for this endpoint",
                }, 500

            permissions = cls.permissions.get(func.__name__)
            if "*" in permissions:
                return func(cls, *args, **kwargs)

            if not is_authenticated():
                return {"status": "error", "msg": "User is not authenticated"}, 401

            user_permissions = get_permissions()
            if any([p in user_permissions for p in permissions]):
                return func(cls, *args, **kwargs)

            return {"status": "error", "msg": "User is not authorized"}, 403
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 500

    return wrapper_decorator


def set_db_user_id(session, transaction, connection, *args, **kwargs):
    try:
        if not is_authenticated():
            raise Exception("User is not authenticated")

        roles = ";".join(get_user_roles())
        stmt = f"EXEC sp_set_session_context 'user_roles', N'{roles}'"
        connection.execute(text(stmt))
    except Exception:
        pass
