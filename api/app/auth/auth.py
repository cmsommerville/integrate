import bcrypt
import random
import functools
from flask import session
from sqlalchemy.sql import text
from app.extensions import db, ma
from app.auth.models import (
    Model_AuthUser,
    Model_AuthRole,
    Model_AuthUserRole,
    Model_AuthUserPasswordHistory,
)
from app.auth import constants
from app.auth.errors import AuthenticationError
from app.auth.constants import (
    DIGITS,
    UPPERCASE_CHARACTERS,
    LOWERCASE_CHARACTERS,
    SYMBOLS,
)
from datetime import datetime, timezone

UNKNOWN_USER = {
    "auth_user_id": None,
    "user_name": "UNKNOWN",
    "roles": [],
    "permissions": [],
    "is_authenticated": False,
    "timestamp": datetime.now(timezone.utc).timestamp() * 1000,
}


class Schema_User_SessionStore(ma.Schema):
    auth_user_id = ma.Integer()
    user_name = ma.String()
    first_name = ma.String()
    last_name = ma.String()
    email_address = ma.String()
    avatar = ma.String(allow_none=True, required=False)
    roles = ma.List(ma.String())
    permissions = ma.List(ma.String())
    direct_reports = ma.List(ma.String())


schema_user_sessionstore = Schema_User_SessionStore()


def check_login_credentials(user_name: str, password: str):
    """
    Checks if the password is correct for the given user name.

    Returns True if the password is correct, False otherwise.
    """
    if not isinstance(user_name, str):
        raise ValueError("Invalid user name")
    if not isinstance(password, str):
        raise ValueError("Invalid password")
    user = Model_AuthUser.find_by_user_name(user_name)

    if user is None:
        return False
    return bcrypt.checkpw(bytes(password, "utf-8"), user.hashed_password)


def validate_unhashed_password(password: str, user: Model_AuthUser = None):
    if password is None:
        raise ValueError("Must provide a password")
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    if len(password) < constants.PASSWORD_MIN_LENGTH:
        raise ValueError("Password must be at least 8 characters long")
    if constants.PASSWORD_REQUIRES_NUMBER and not any(
        char.isdigit() for char in password
    ):
        raise ValueError("Password must contain at least one number")
    if constants.PASSWORD_REQUIRES_UPPERCASE and not any(
        char.isupper() for char in password
    ):
        raise ValueError("Password must contain at least one uppercase letter")
    if constants.PASSWORD_REQUIRES_LOWERCASE and not any(
        char.islower() for char in password
    ):
        raise ValueError("Password must contain at least one lowercase letter")
    if constants.PASSWORD_REQUIRES_SPECIAL_CHAR and not any(
        char in SYMBOLS for char in password
    ):
        raise ValueError("Password must contain at least one special character")

    # validate password against user's password history
    if user is not None and getattr(user, "password_list", []):
        if next(
            (
                True
                for pw in user.password_list
                if bcrypt.checkpw(bytes(password, "utf-8"), pw)
            ),
            False,
        ):
            raise ValueError("Password cannot be the same as the last 5 passwords")


def generate_password(password_length=12):
    """
    Generate a random password of the given length.
    """
    VALID_CHARACTERS = DIGITS + UPPERCASE_CHARACTERS + LOWERCASE_CHARACTERS + SYMBOLS
    new_password = "".join(
        [random.choice(VALID_CHARACTERS) for _ in range(password_length)]
    )
    try:
        validate_unhashed_password(new_password)
    except ValueError:
        new_password = generate_password(password_length)
    return new_password


def register_user(user_data):
    """
    This function registers a new user with the given user name and password.
    It performs all password validation, hashing, and accepts a list of roles too.
    """
    check_existing_user = Model_AuthUser.find_by_user_name(user_data["user_name"])
    if check_existing_user is not None:
        raise ValueError("User name already exists")

    password = user_data.pop("password")
    validate_unhashed_password(password)
    bytes_password = bytes(password, "utf-8")
    hashed_password = bcrypt.hashpw(
        bytes_password, bcrypt.gensalt(constants.BCRYPT_ROUNDS_WORK_FACTOR)
    )

    roles = user_data.pop("roles", [])
    role_objs = Model_AuthRole.find_by_code(roles)
    user_roles = [
        Model_AuthUserRole(auth_role_id=role.auth_role_id) for role in role_objs
    ]

    user = Model_AuthUser(
        **user_data, hashed_password=hashed_password, roles=user_roles
    )
    user.password_history.append(
        Model_AuthUserPasswordHistory(
            auth_user_id=user.auth_user_id, hashed_password=hashed_password
        )
    )
    try:
        db.session.add(user)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    return user


def update_password(
    user_name: str, password: str, confirm_password: str
) -> Model_AuthUser:
    """
    This function updates a user's password. It performs all password validation and hashing.
    """
    user = Model_AuthUser.find_by_user_name(user_name)
    if user is None:
        raise ValueError("User name does not exist")

    if password != confirm_password:
        raise ValueError("Passwords do not match")

    validate_unhashed_password(password, user=user)
    bytes_password = bytes(password, "utf-8")
    hashed_password = bcrypt.hashpw(
        bytes_password, bcrypt.gensalt(constants.BCRYPT_ROUNDS_WORK_FACTOR)
    )

    try:
        user.hashed_password = hashed_password
        user.password_last_changed_dt = db.func.current_timestamp()
        user.password_history.append(
            Model_AuthUserPasswordHistory(
                auth_user_id=user.auth_user_id, hashed_password=hashed_password
            )
        )
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    return user


def validate_user(user):
    if user.get("auth_user_id") is None:
        raise ValueError("User must have auth_user_id key")
    if user.get("user_name") is None:
        raise ValueError("User must have user_name key")
    if not isinstance(user.get("roles"), list):
        raise ValueError("User must have roles key")
    return schema_user_sessionstore.load(user)


def get_user():
    if session.get("user", None) is None:
        raise AuthenticationError("User has not been authenticated. Please login.")
    return session["user"]


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

        user = get_user()
        if user is None:
            raise Exception("User is not authenticated")
        user_name = user.get("user_name")
        stmt = f"EXEC sp_set_session_context 'user_name', N'{user_name}'"
        connection.execute(text(stmt))
    except Exception:
        pass
