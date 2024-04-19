from flask_restx import Resource
from ..auth import get_user


class Resource_AuthGetUser(Resource):
    @classmethod
    def get(cls):
        try:
            user = get_user()
            return user, 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
