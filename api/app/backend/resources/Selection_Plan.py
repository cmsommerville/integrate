from typing import Union
from flask import request
from flask_restx import Resource
from app.auth import authorization_required
from app.shared import BaseCRUDResource, BaseCRUDResourceList, BaseValidator
from ..models import Model_SelectionPlan
from ..schemas import Schema_SelectionPlan


class CRUD_SelectionPlan(BaseCRUDResource):
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan()


class CRUD_SelectionPlan_CreateOnly(Resource):
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan()
    validator: Union[BaseValidator, None] = None
    permissions: dict = {
        "post": ["*"],
    }

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
    def create(cls, *args, **kwargs):
        req = request.get_json()
        if cls.validator:
            cls.validator.create(req)
        obj = cls.schema.load(req)
        obj.save_to_db()
        return cls.schema.dump(obj)


class CRUD_SelectionPlan_List(BaseCRUDResourceList):
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan(many=True)
