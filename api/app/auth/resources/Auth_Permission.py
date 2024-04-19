from flask import request
from flask_restx import Resource
from ..models import Model_AuthPermission
from ..schemas import Schema_AuthPermission

_schema_list = Schema_AuthPermission(many=True)


class Resource_AuthPermissions(Resource):
    @classmethod
    def get(self):
        try:
            permissions = Model_AuthPermission.find_all()
            return _schema_list.dump(permissions), 200
        except Exception:
            return {"status": "error", "msg": "Cannot get permissions"}, 400

    def post(self):
        try:
            data = request.get_json()
            permissions = _schema_list.load(data)
            Model_AuthPermission.save_all_to_db(permissions)
            return _schema_list.dump(permissions), 201
        except Exception:
            return {"status": "error", "msg": "Cannot save permissions"}, 400
