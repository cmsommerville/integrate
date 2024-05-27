from flask_restx import Resource
from app.auth.auth import (
    get_user,
)


class Resource_GetCurrentUser(Resource):
    """
    This resource is for sys admins to create new users
    """

    @classmethod
    def get(cls):
        try:
            user = get_user()
            return user, 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
