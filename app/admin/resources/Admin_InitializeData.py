import os
import json
from flask import request, current_app
from flask_marshmallow import Schema
from flask_restx import Resource, fields
from app.extensions import db
from app.shared import BaseTemporalTable
from app.backend.data import load_refdata, load_config


class Resource_AdminInitRefData(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_refdata(hostname)
        return {"status": "success", "message": "Reference tables successfully loaded"}


class Resource_AdminInitConfig(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_config(hostname)
        return {"status": "success", "message": "Config tables successfully loaded"}


