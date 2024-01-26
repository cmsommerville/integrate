from flask import request
from flask_restx import Resource
from .BaseModel import BaseModel
from .BaseSchema import BaseSchema
from app.auth import authorization_required


class BaseCRUDResource(Resource):
    model: BaseModel
    schema: BaseSchema
    model_args: dict = {}
    permissions: dict = {
        "get": ["*"],
        "post": ["*"],
        "patch": ["*"],
        "put": ["*"],
        "delete": ["*"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    @authorization_required(permissions.get("get"))
    def get(cls, id, *args, **kwargs):
        try:
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception:
            return {}, 200

        return cls.schema.dump(obj), 200

    @classmethod
    @authorization_required(permissions.get("post"))
    def post(cls, *args, **kwargs):
        try:
            req = request.get_json()
            obj = cls.schema.load(req)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required(permissions.get("put"))
    def put(cls, *args, **kwargs):
        try:
            req = request.get_json()
            obj = cls.schema.load(req)
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required(permissions.get("patch"))
    def patch(cls, id, *args, **kwargs):
        try:
            req = request.get_json()
            # get existing data
            obj = cls.model.find_one(id, **cls.model_args)
            data = cls.schema.dump(obj)
            for attr, val in req.items():
                data[attr] = val
            # save object to database
            new = cls.schema.load(data)
            new.save_to_db()
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(new), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required(permissions.get("delete"))
    def delete(cls, id, *args, **kwargs):
        try:
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            obj.delete()
            return {"status": "Deleted"}, 204
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400


class BaseCRUDResourceList(Resource):
    model: BaseModel
    schema: BaseSchema
    model_args: dict = {}
    permissions: dict = {
        "get": ["*"],
        "post": ["*"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    @authorization_required(permissions.get("get"))
    def get(cls, *args, **kwargs):
        try:
            objs = cls.model.find_all(**cls.model_args)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            if objs:
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception:
            return [], 200

    @classmethod
    @authorization_required(permissions.get("post"))
    def post(cls, *args, **kwargs):
        try:
            req = request.get_json()
            objs = cls.schema.load(req)
            cls.model.save_all_to_db(objs)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(objs), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
