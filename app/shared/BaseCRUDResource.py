from typing import Union
from flask import request
from flask_restx import Resource
from .BaseModel import BaseModel
from .BaseSchema import BaseSchema
from .BaseValidator import BaseValidator, BaseListValidator
from app.auth import authorization_required
from .RateEngine import RateEngine


class BaseCRUDResource(Resource):
    model: BaseModel
    schema: BaseSchema
    validator: Union[BaseValidator, None] = None
    permissions: dict = {
        "get": ["*"],
        "post": ["*"],
        "patch": ["*"],
        "put": ["*"],
        "delete": ["*"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @authorization_required
    def get(cls, id, *args, **kwargs):
        try:
            data = cls.retrieve(id, *args, **kwargs)
            return data, 200
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required
    def post(cls, *args, **kwargs):
        try:
            data = cls.create(*args, **kwargs)
            return data, 201
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required
    def put(cls, id, *args, **kwargs):
        try:
            data = cls.replace(id, *args, **kwargs)
            return data, 201
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required
    def patch(cls, id, *args, **kwargs):
        try:
            data = cls.update(id, *args, **kwargs)
            return data, 201
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required
    def delete(cls, id, *args, **kwargs):
        try:
            cls.destroy(id, *args, **kwargs)
            return {"status": "success", "msg": "Successfully deleted"}
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def retrieve(cls, id, *args, **kwargs):
        obj = cls.model.find_one(id, *args, **kwargs)
        return cls.schema.dump(obj)

    @classmethod
    def create(cls, *args, **kwargs):
        req = request.get_json()
        if cls.validator:
            cls.validator.create(req)
        obj = cls.schema.load(req)
        obj.save_to_db()
        return cls.schema.dump(obj)

    @classmethod
    def replace(cls, id, *args, **kwargs):
        req = request.get_json()
        if cls.validator:
            cls.validator.replace(req)
        obj = cls.model.replace_one(id, req)
        return cls.schema.dump(obj)

    @classmethod
    def update(cls, id, *args, **kwargs):
        req = request.get_json()
        if cls.validator:
            cls.validator.update(req)
        obj = cls.model.update_one(id, req)
        return cls.schema.dump(obj)

    @classmethod
    def destroy(cls, id, *args, **kwargs):
        obj = cls.model.find_one(id, *args, **kwargs)
        obj.delete()


class BaseCRUDResourceList(Resource):
    model: BaseModel
    schema: BaseSchema
    validator: Union[BaseListValidator, None] = None
    permissions: dict = {
        "get": ["*"],
        "post": ["*"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @authorization_required
    def get(cls, *args, **kwargs):
        try:
            data = cls.list(*args, **kwargs)
            return data, 200
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    @authorization_required
    def post(cls, *args, **kwargs):
        try:
            data = cls.bulk_create(*args, **kwargs)
            return data, 201
        except NotImplementedError as e:
            return {"status": "error", "msg": str(e)}, 405
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def list(cls, *args, **kwargs):
        objs = cls.model.find_all(*args, **kwargs)
        return cls.schema.dump(objs)

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        req = request.get_json()
        if cls.validator:
            cls.validator.bulk_create(req)
        objs = cls.schema.load(req)
        cls.model.save_all_to_db(objs)
        return cls.schema.dump(objs)


class BaseSelectionCRUDResource(BaseCRUDResource):
    @classmethod
    def create(cls, plan_id: int, *args, **kwargs):
        event = f"create:{getattr(cls, 'EVENT', cls.__name__)}"
        data = super().create(*args, **kwargs)
        rater = RateEngine(plan_id, event)
        rater.calculate()
        return data

    @classmethod
    def update(cls, id: int, plan_id: int, *args, **kwargs):
        event = f"update:{getattr(cls, 'EVENT', cls.__name__)}"
        data = super().update(id, *args, **kwargs)
        rater = RateEngine(plan_id, event)
        rater.calculate()
        return data

    @classmethod
    def replace(cls, id: int, plan_id: int, *args, **kwargs):
        event = f"replace:{getattr(cls, 'EVENT', cls.__name__)}"
        data = super().replace(id, *args, **kwargs)
        rater = RateEngine(plan_id, event)
        rater.calculate()
        return data

    @classmethod
    def destroy(cls, id: int, plan_id: int, *args, **kwargs):
        event = f"destroy:{getattr(cls, 'EVENT', cls.__name__)}"
        super().replace(id, *args, **kwargs)
        rater = RateEngine(plan_id, event)
        rater.calculate()
        return None


class BaseSelectionCRUDResourceList(BaseCRUDResourceList):
    @classmethod
    def bulk_create(cls, plan_id: int, *args, **kwargs):
        event = f"bulk_create:{getattr(cls, 'EVENT', cls.__name__)}"
        data = super().bulk_create(*args, **kwargs)
        rater = RateEngine(plan_id, event)
        rater.calculate()
        return data
