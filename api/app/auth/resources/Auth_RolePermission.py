from flask import request
from flask_restx import Resource
from ..models import Model_AuthPermission, Model_AuthRole, Model_AuthRolePermission
from ..schemas import Schema_AuthRolePermission

_schema_list = Schema_AuthRolePermission(many=True)


class Resource_AuthManageRolePermissions(Resource):
    @classmethod
    def post(cls, id):
        try:
            data = request.get_json()
            _permissions = data.get("permissions")
            if _permissions is None:
                return {
                    "status": "error",
                    "msg": "Please send a list of permissions",
                }, 400
            try:
                permissions = Model_AuthPermission.find_by_code(_permissions)
            except Exception:
                return {"status": "error", "msg": "Cannot find permissions"}, 400

            try:
                role = Model_AuthRole.find_one(id)
                existing_permission_ids = [
                    r.auth_permission_id for r in role.permissions
                ]
                new_role_permissions = [
                    {
                        "auth_permission_id": p.auth_permission_id,
                        "auth_role_id": role.auth_role_id,
                    }
                    for p in permissions
                    if p.auth_permission_id not in existing_permission_ids
                ]
                role_permissions = _schema_list.load(new_role_permissions)
                Model_AuthRolePermission.save_all_to_db(role_permissions)

                return _schema_list.dump(role_permissions), 201
            except Exception:
                return {"status": "error", "msg": "Cannot add permissions to role"}, 401

        except Exception:
            return {"status": "error", "msg": "Unknown add role permission error"}, 400
