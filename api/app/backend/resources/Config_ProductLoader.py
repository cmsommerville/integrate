from flask import request
from flask_restx import Resource
from ..classes.ConfigProductLoader import ConfigProductLoader


class Resource_ConfigProductLoader(Resource):
    def post(self):
        try:
            data = request.get_json()
            loader = ConfigProductLoader(config=data)
            loader.save_to_db()
            return {"status": "success", "msg": "Product loaded"}
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 500
