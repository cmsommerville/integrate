from flask import request
from flask_restx import Resource
from app.auth.models import Model_AuthRole, Model_AuthUser


class Resource_AdminAssignUserRole(Resource):

    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400

            roles = data.get('roles')
            if not isinstance(roles, list):
                return {"status": "error", "msg": "Please provide a list of roles"}, 400
            if len(roles) == 0: 
                return {"status": "error", "msg": "Please provide at least one role"}, 400

            user = Model_AuthUser.find_by_user_name(user_name)
            if user is None:
                return {"status": "error", "msg": f"Cannot find user with user name {user_name}"}, 400

            existing_roles = [role.role_name for role in user.roles]
            user.roles = [
                *user.roles, 
                *[
                    Model_AuthRole(**{
                        'user_id': user.user_id, 
                        'role_name': role
                    }) 
                for role in roles if role not in existing_roles]
            ]
            user.save_to_db()
        except Exception as e:
            return str(e), 400
        else:
            return {"status": "success", "msg": "Added roles to user"}, 201


class Resource_AdminRemoveUserRole(Resource):

    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None:
                return {"status": "error", "msg": "Please provide user name"}, 400

            roles = data.get('roles')
            if not isinstance(roles, list):
                return {"status": "error", "msg": "Please provide a list of roles"}, 400
            if len(roles) == 0: 
                return {"status": "error", "msg": "Please provide at least one role"}, 400

            user = Model_AuthUser.find_by_user_name(user_name)
            if user is None:
                return {"status": "error", "msg": f"Cannot find user with user name {user_name}"}, 400
            delete_roles = [
                role for role in user.roles if role.role_name in roles
            ]
            Model_AuthRole.delete(delete_roles)
        except Exception as e:
            return str(e), 400
        else:
            return {"status": "success", "msg": "Removed requested roles from user"}, 201

