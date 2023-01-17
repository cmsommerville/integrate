import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from ..models import Model_AuthUser, Model_AuthRole, Model_AuthUserRole
from ..schemas import Schema_AuthUserRole
from ..constants import BCRYPT_ROUNDS_WORK_FACTOR

_schema_list = Schema_AuthUserRole(many=True)

class Resource_AuthManageUserRole(Resource): 
    
    @classmethod
    def post(cls):
        try: 
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None: 
                return {"status": "error", "msg": "Please send a user name"}, 400

            _roles = data.get('roles')
            if _roles is None: 
                return {"status": "error", "msg": "Please send a list of roles"}, 400
            try:
                roles = Model_AuthRole.find_by_code(_roles)
            except:
                return {"status": "error", "msg": "Cannot find roles"}, 400

            try:
                user = Model_AuthUser.find_by_user_name(user_name)
                existing_role_ids = [r.auth_role_id for r in user.roles]
                new_user_roles = [
                    {
                        "auth_user_id": user.auth_user_id, 
                        "auth_role_id": r.auth_role_id, 
                    } 
                    for r in roles 
                    if r.auth_role_id not in existing_role_ids
                ]
                user_roles = _schema_list.load(new_user_roles)
                Model_AuthUserRole.save_all_to_db(user_roles)

                return _schema_list.dump(user_roles), 201
            except:
                return {"status": "error", "msg": "Cannot add roles to user"}, 401

        except:
            return {"status": "error", "msg": "Unknown add role error"}, 400