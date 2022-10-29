import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser
from ..constants import BCRYPT_ROUNDS_WORK_FACTOR

_schema = Schema_AuthUser()


class Resource_AuthRegister(Resource): 
    
    @classmethod
    def post(cls):
        try: 
            data = request.get_json()
            user_name = data.get('user_name')
            if user_name is None: 
                return {"status": "error", "message": "Please send a user name"}
            check_existing_user = Model_AuthUser.find_by_user_name(user_name)
            if check_existing_user is not None:
                return {"status": "error", "message": "User name already exists"}

            password = data.get('password')
            if password is None: 
                return {"status": "error", "message": "Please send a password"}

            bytes_password = bytes(password, 'utf-8')

            hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt(BCRYPT_ROUNDS_WORK_FACTOR))
            user = _schema.load({
                'user_name': user_name,
                'hashed_password': hashed_password
            })

            user.save_to_db()
            user_data = _schema.dump(user)
            access_token = create_access_token(identity=user_data)
            return {"token": access_token}, 201

        except Exception as e:
            return {"status": "error", "message": "Unknown login error", "traceback": str(e)}, 400