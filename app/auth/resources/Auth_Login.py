import bcrypt
from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from ..extensions import auth
from ..models import Model_AuthUser
from ..schemas import Schema_AuthUser_JWT

_schema = Schema_AuthUser_JWT()

@auth.route('/login', methods=['POST'])
def login():
    try: 
        data = request.get_json()
        user_name = data.get('user_name')
        if user_name is None: 
            return jsonify({"login": False, "status": "error", "msg": "Please send a user name"}), 400

        password = data.get('password')
        if password is None: 
            return jsonify({"login": False, "status": "error", "msg": "Please send a password"}), 400

        user = Model_AuthUser.find_by_user_name(user_name)
        is_password_correct = bcrypt.checkpw(bytes(password, 'utf-8'), user.hashed_password)
        user_data = _schema.dump(user)

        if is_password_correct:
            access_token = create_access_token(identity=user_data)
            refresh_token = create_refresh_token(identity=user_data)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)  
            set_refresh_cookies(resp, refresh_token)
            return resp, 200

        else:
            return jsonify({"login": False, "status": "error", "msg": "Password incorrect"}), 401
    except:
        return jsonify({"login": False, "status": "error", "msg": "Unknown login error"}), 400

class Resource_AuthLogin(Resource): 
    
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

            user = Model_AuthUser.find_by_user_name(user_name)
            is_password_correct = bcrypt.checkpw(bytes(password, 'utf-8'), user.hashed_password)
            user_data = _schema.dump(user)

            if is_password_correct:
                access_token = create_access_token(identity=user_data)
                refresh_token = create_refresh_token(identity=user_data)
                resp = jsonify({'login': True})
                set_access_cookies(resp, access_token)  
                set_refresh_cookies(resp, refresh_token)
                return resp, 200
            else:
                return {"status": "error", "msg": "Password incorrect"}, 401

        except:
            return {"status": "error", "msg": "Unknown login error"}, 400