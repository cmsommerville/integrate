import bcrypt
from flask import request, session
from flask_restx import Resource
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser_Output
from ..constants import BCRYPT_ROUNDS_WORK_FACTOR
from ..auth import is_authenticated, login_user, logout

_schema = Schema_AuthUser_Output()


class Resource_AuthSetPassword(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            if user_name is None:
                session["is_authenticated"] = False
                return {"status": "error", "msg": "Please send a user name"}

            password = data.get("password")
            if password is None:
                session["is_authenticated"] = False
                return {"status": "error", "msg": "Please send a password"}

            bytes_password = bytes(password, "utf-8")
            hashed_password = bcrypt.hashpw(
                bytes_password, bcrypt.gensalt(BCRYPT_ROUNDS_WORK_FACTOR)
            )

            try:
                user = Model_AuthUser.find_by_user_name(user_name)
                user.hashed_password = hashed_password
                user.save_to_db()
                login_user(user)

                if is_authenticated():
                    return {
                        "status": "success",
                        "msg": "Password changed successfully",
                    }, 200
                return {"status": "error", "msg": "Cannot update password"}, 401
            except Exception:
                logout()
                return {"status": "error", "msg": "Cannot update password"}, 401

        except Exception:
            logout()
            return {"status": "error", "msg": "Unknown set password error"}, 400
