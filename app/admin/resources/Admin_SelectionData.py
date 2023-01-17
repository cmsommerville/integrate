import os
import json
from flask import request, current_app
from flask_marshmallow import Schema
from flask_restx import Resource, fields
from app.extensions import db
from app.shared import BaseTemporalTable
from app.backend.data import load_selection


class Resource_AdminSelectionData(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_selection(hostname, headers=request.headers)
        return {"status": "success", "msg": "Selections successfully loaded"}
