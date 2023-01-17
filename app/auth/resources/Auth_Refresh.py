from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies)
from ..extensions import auth

# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    refresh_token = create_refresh_token(identity=identity)
    res = jsonify({'login': True})
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)
    return res, 200