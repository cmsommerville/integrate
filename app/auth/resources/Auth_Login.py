import bcrypt
from flask import request
from flask_restx import Resource
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser_Output
from ..auth import login_user, logout, is_authenticated


_schema = Schema_AuthUser_Output()


class Resource_AuthLogin(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            user = Model_AuthUser.find_by_user_name(user_name)
            password = data.get("password")
            is_valid_password = bcrypt.checkpw(
                bytes(password, "utf-8"), user.hashed_password
            )
            if is_valid_password:
                login_user(user)

            if is_authenticated():
                return {"status": "success", "msg": "Successfully logged in"}, 200
            return {"status": "error", "msg": "Password incorrect"}, 401

        except Exception:
            logout()
            return {"status": "error", "msg": "Unknown login error"}, 400
