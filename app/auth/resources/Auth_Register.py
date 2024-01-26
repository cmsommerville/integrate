import bcrypt
from flask import request
from flask_restx import Resource
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser
from ..constants import BCRYPT_ROUNDS_WORK_FACTOR
from ..auth import login_user, logout, is_authenticated

_schema = Schema_AuthUser()


class Resource_AuthRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            if user_name is None:
                return {"status": "error", "msg": "Please send a user name"}
            check_existing_user = Model_AuthUser.find_by_user_name(user_name)
            if check_existing_user is not None:
                return {"status": "error", "msg": "User name already exists"}

            password = data.get("password")
            if password is None:
                return {"status": "error", "msg": "Please send a password"}

            bytes_password = bytes(password, "utf-8")

            hashed_password = bcrypt.hashpw(
                bytes_password, bcrypt.gensalt(BCRYPT_ROUNDS_WORK_FACTOR)
            )
            user = _schema.load(
                {"user_name": user_name, "hashed_password": hashed_password}
            )

            user.save_to_db()
            login_user(user)
            if is_authenticated() is True:
                return {"status": "success", "msg": "Successfully registered"}, 200

            return {"status": "error", "msg": "Unknown registration error"}, 401

        except Exception as e:
            logout()
            return {
                "status": "error",
                "msg": "Unknown login error",
                "traceback": str(e),
            }, 400
