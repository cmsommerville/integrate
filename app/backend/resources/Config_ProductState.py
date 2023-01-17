from flask import request
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductState
from ..schemas import Schema_ConfigProductState

class CRUD_ConfigProductState(BaseCRUDResource): 
    model = Model_ConfigProductState
    schema = Schema_ConfigProductState()

class CRUD_ConfigProductState_List(BaseCRUDResourceList): 
    model = Model_ConfigProductState
    schema = Schema_ConfigProductState(many=True)

    @classmethod
    def get(cls, product_id: int, *args, **kwargs):
        try: 
            objs = cls.model.find_by_product(product_id)
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('get', objs, request)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try: 
            if objs: 
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception as e:
            return [], 200