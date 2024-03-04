import os
from flask import request
from flask_restx import Resource
from app.backend.data import load_refdata, load_config, load_generic
from app.backend.classes.ConfigProductLoader import ConfigProductLoader


class Resource_AdminLoadData(Resource):
    @classmethod
    def post(cls):
        hostname = os.getenv("HOSTNAME")
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_generic(hostname, headers=request.headers)
        return {"status": "success", "msg": "Reference tables successfully loaded"}


class Resource_AdminInitRefData(Resource):
    @classmethod
    def post(cls):
        hostname = os.getenv("HOSTNAME")
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_refdata(hostname, headers=request.headers)
        return {"status": "success", "msg": "Reference tables successfully loaded"}


class Resource_AdminInitConfig(Resource):
    @classmethod
    def post(cls):
        hostname = os.getenv("HOSTNAME")
        if not hostname:
            return {"error": "Could not find HOSTNAME environment variable"}, 400
        load_config(hostname, headers=request.headers)
        return {"status": "success", "msg": "Config tables successfully loaded"}


class Resource_ConfigProductLoader(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            attr = request.args.get("attr", "product_data")
            loader = ConfigProductLoader(data)
            loader.save_to_db()
            return getattr(loader, attr), 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
