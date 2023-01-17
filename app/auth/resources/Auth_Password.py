import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser_JWT
from ..constants import BCRYPT_ROUNDS_WORK_FACTOR

_schema = Schema_AuthUser_JWT()

class Resource_AuthSetPassword(Resource): 
    
    @classmethod
    def post(cls):
        try: 
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None: 
                return {"status": "error", "msg": "Please send a user name"}

            password = data.get('password')
            if password is None: 
                return {"status": "error", "msg": "Please send a password"}

            bytes_password = bytes(password, 'utf-8')
            hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt(BCRYPT_ROUNDS_WORK_FACTOR))


            try:
                user = Model_AuthUser.find_by_user_name(user_name)
                user.hashed_password = hashed_password
                user.save_to_db()

                return {"status": "success", "msg": "Password changed successfully"}, 200
            except:
                return {"status": "error", "msg": "Cannot update password"}, 401

        except:
            return {"status": "error", "msg": "Unknown set password error"}, 400