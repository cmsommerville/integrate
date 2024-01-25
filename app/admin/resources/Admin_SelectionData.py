import os
from flask import request
from flask_restx import Resource
from app.backend.data import load_selection


class Resource_AdminSelectionData(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_selection(hostname, headers=request.headers)
        return {"status": "success", "msg": "Selections successfully loaded"}
