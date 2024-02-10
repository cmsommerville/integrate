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
    @authorization_required
    def get(cls, *args, **kwargs):
        return cls.retrieve(*args, **kwargs)

    @classmethod
    @authorization_required
    def post(cls, *args, **kwargs):
        return cls.create(*args, **kwargs)

    @classmethod
    @authorization_required
    def put(cls, *args, **kwargs):
        return cls.replace(*args, **kwargs)

    @classmethod
    @authorization_required
    def patch(cls, id, *args, **kwargs):
        return cls.update(id, *args, **kwargs)

    @classmethod
    @authorization_required
    def delete(cls, id, *args, **kwargs):
        return cls.destroy(id, *args, **kwargs)

    @classmethod
    def retrieve(cls, id, *args, **kwargs):
        try:
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception:
            return {}, 200
        return cls.schema.dump(obj), 200

    @classmethod
    def create(cls, *args, **kwargs):
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
    def replace(cls, id, *args, **kwargs):
        try:
            req = request.get_json()
            obj = cls.model.replace_one(id, req)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def update(cls, id, *args, **kwargs):
        try:
            req = request.get_json()
            obj = cls.model.update_one(id, req)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def destroy(cls, id, *args, **kwargs):
        try:
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            obj.delete()
            return {"status": "Deleted"}, 200
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
    @authorization_required
    def get(cls, *args, **kwargs):
        return cls.list(*args, **kwargs)

    @classmethod
    @authorization_required
    def post(cls, *args, **kwargs):
        return cls.bulk_create(*args, **kwargs)

    @classmethod
    def list(cls, *args, **kwargs):
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
    def bulk_create(cls, *args, **kwargs):
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
