from flask import request
from flask_restx import Resource
from app.auth.models import Model_AuthRole, Model_AuthUser, Model_AuthUserRole
from app.auth.auth import (
    authorization_required,
    register_user,
    get_user,
    update_password,
    generate_password,
)
from app.auth.schemas import Schema_NewUser


class Resource_AdminCreateNewUser(Resource):
    """
    This resource is for sys admins to create new users
    """

    schema = Schema_NewUser()
    permissions = {"post": ["admin"]}

    @classmethod
    @authorization_required
    def post(cls):
        try:
            data = request.get_json()
            validated_data = cls.schema.load(data)
            register_user(validated_data)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
        else:
            return {"status": "success", "msg": "Added user"}, 201


class Resource_AdminResetUserPassword(Resource):
    permissions = {"post": ["admin"]}

    @classmethod
    @authorization_required
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            new_password = data.get("new_password")
            if new_password is None:
                new_password = generate_password()

            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400

            update_password(user_name, new_password, new_password)
            return {
                "status": "success",
                "msg": f"Password reset to `{new_password}`",
            }, 201

        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400


class Resource_AdminAssignUserRole(Resource):
    permissions = {"post": ["admin"]}

    @classmethod
    @authorization_required
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400

            roles = data.get("roles")
            if not isinstance(roles, list):
                return {"status": "error", "msg": "Please provide a list of roles"}, 400
            if len(roles) == 0:
                return {
                    "status": "error",
                    "msg": "Please provide at least one role",
                }, 400

            user = Model_AuthUser.find_by_user_name(user_name)
            if user is None:
                return {
                    "status": "error",
                    "msg": f"Cannot find user with user name {user_name}",
                }, 400

            role_objs = Model_AuthRole.find_by_code(roles)
            role_codes = [role.auth_role_code for role in role_objs]
            if any([r not in role_codes for r in roles]):
                return {
                    "status": "error",
                    "msg": "Cannot find all role(s) in the database",
                }

            existing_user_role_codes = [
                user_role.role.auth_role_code for user_role in user.roles
            ]
            new_roles = [
                Model_AuthUserRole(
                    auth_user_id=user.auth_user_id, auth_role_id=role.auth_role_id
                )
                for role in role_objs
                if role.auth_role_code not in existing_user_role_codes
            ]
            user.roles.extend(new_roles)
            user.save_to_db()
        except Exception as e:
            return str(e), 400
        else:
            return {"status": "success", "msg": "Added roles to user"}, 201


class Resource_AdminRemoveUserRole(Resource):
    permissions = {"post": ["admin"]}

    @classmethod
    @authorization_required
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get("user_name")
            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400

            roles = data.get("roles")
            if not isinstance(roles, list):
                return {"status": "error", "msg": "Please provide a list of roles"}, 400
            if len(roles) == 0:
                return {
                    "status": "error",
                    "msg": "Please provide at least one role",
                }, 400

            user = Model_AuthUser.find_by_user_name(user_name)
            if user is None:
                return {
                    "status": "error",
                    "msg": f"Cannot find user with user name {user_name}",
                }, 400
            delete_roles = [role for role in user.roles if role.role_name in roles]
            Model_AuthRole.delete(delete_roles)
        except Exception as e:
            return str(e), 400
        else:
            return {
                "status": "success",
                "msg": "Removed requested roles from user",
            }, 201
