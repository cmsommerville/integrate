import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from ..models import Model_AuthRole
from ..schemas import Schema_AuthRole

_schema_list = Schema_AuthRole(many=True)

class Resource_AuthRoles(Resource): 
    
    @classmethod
    def get(self):
        try: 
            roles = Model_AuthRole.find_all()
            return _schema_list.dump(roles), 200
        except:
            return {"status": "error", "msg": "Cannot get roles"}, 400

    def post(self):
        try: 
            data = request.get_json()
            roles = _schema_list.load(data)
            Model_AuthRole.save_all_to_db(roles)
            return _schema_list.dump(roles), 201
        except:
            return {"status": "error", "msg": "Cannot save roles"}, 400