import functools
from flask import session
from datetime import datetime, timezone


def validate_user(user):
    if user.get("user_id") is None:
        raise ValueError("User must have user_id key")
    if not isinstance(user.get("roles"), list):
        raise ValueError("User must have roles key")
    return {
        "user_id": user.get("user_id"),
        "roles": user.get("roles"),
    }


def login_user(user):
    try:
        user_data = validate_user(user)
        session["user"] = {
            "user": user_data,
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
    return session.get("user", {}).get("user", {}).get("roles", [])


def login_required(**kw):
    def outer(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if is_authenticated():
                return func(*args, **kwargs)
            return {"status": "error", "msg": "User is not authenticated"}, 401

        return wrapper_decorator

    return outer


def authorization_required(permissions: list, **kw):
    def outer(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if "*" in permissions:
                return func(*args, **kwargs)

            if not is_authenticated():
                return {"status": "error", "msg": "User is not authenticated"}, 401

            user_permissions = get_permissions()
            if any([p in user_permissions for p in permissions]):
                return func(*args, **kwargs)

            return {"status": "error", "msg": "User is not authorized"}, 403

        return wrapper_decorator

    return outer


def set_db_user_id(session, transaction, connection, *args, **kwargs):
    try:
        if not is_authenticated():
            raise Exception("User is not authenticated")

        roles = ";".join(get_user_roles())
        stmt = f"EXEC sp_set_session_context 'user_roles', N'{roles}'"
        connection.execute(stmt)
    except Exception:
        pass
