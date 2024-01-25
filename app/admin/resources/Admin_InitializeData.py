import os
from flask import request
from flask_restx import Resource
from app.backend.data import load_rate_table, load_refdata, load_config


class Resource_AdminInitRefData(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_refdata(hostname, headers=request.headers)
        return {"status": "success", "msg": "Reference tables successfully loaded"}


class Resource_AdminInitConfig(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_config(hostname, headers=request.headers)
        return {"status": "success", "msg": "Config tables successfully loaded"}



class Resource_AdminInitRateTable(Resource):

    @classmethod
    def post(cls):
        hostname = os.getenv('HOSTNAME')
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_rate_table(hostname, headers=request.headers)
        return {"status": "success", "msg": "Rate tables successfully loaded"}

