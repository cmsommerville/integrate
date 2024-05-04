from flask import request
from flask_restx import Resource, fields
from app.extensions import api
from app.auth.auth import (
    login_user,
    update_password,
    check_login_credentials,
)
from app.auth.schemas import Schema_AuthUser_Output


schema_auth_user = Schema_AuthUser_Output()


model_post = api.model(
    "Resource_AuthSetPassword_POST",
    {
        "user_name": fields.String(
            description="A valid user name whose password is to be updated",
            required=True,
        ),
        "old_password": fields.String(
            description="The current password of the user",
            required=True,
        ),
        "new_password": fields.String(
            description="The new password that the user wants to change to",
            required=True,
        ),
        "confirm_password": fields.String(
            description="A confirmation of the new password. The new password must match this value",
            required=True,
        ),
    },
)


class Resource_AuthSetPassword(Resource):
    @classmethod
    @api.doc(
        model=model_post,
        validate=True,
        description="Update the password of a user. The user must provide the old password, the new password, and a confirmation of the new password",
    )
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400
            is_valid_password = check_login_credentials(user_name, old_password)
            if is_valid_password:
                # update the password
                user = update_password(user_name, new_password, confirm_password)
                # then reset the user data stored in the session
                user_data = schema_auth_user.dump(user)
                login_user(user_data)
                return {"status": "success", "msg": "Password set"}, 201

            return {"status": "error", "msg": "Old password is invalid"}, 400
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
