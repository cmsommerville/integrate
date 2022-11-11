import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser_JWT

_schema = Schema_AuthUser_JWT()

class Resource_AuthLogin(Resource): 
    
    @classmethod
    def post(cls):
        try: 
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None: 
                return {"status": "error", "message": "Please send a user name"}

            password = data.get('password')
            if password is None: 
                return {"status": "error", "message": "Please send a password"}

            user = Model_AuthUser.find_by_user_name(user_name)
            is_password_correct = bcrypt.checkpw(bytes(password, 'utf-8'), user.hashed_password)
            user_data = _schema.dump(user)

            if is_password_correct:
                access_token = create_access_token(identity=user_data)
                return {"token": access_token}, 200
            else:
                return {"status": "error", "message": "Password incorrect"}, 401

        except:
            return {"status": "error", "message": "Unknown login error"}, 400