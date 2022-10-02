from flask import request
from flask_restx import Resource
from .BaseModel import BaseModel
from .BaseSchema import BaseSchema
from .BaseObservable import BaseObservable

class BaseCRUDResource(Resource):
    model: BaseModel
    schema: BaseSchema
    observable: BaseObservable = None
    model_args: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def get(cls, id, *args, **kwargs):
        try: 
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception as e:
            return {}, 200
        
        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('get', obj, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        return cls.schema.dump(obj), 200
  
    @classmethod  
    def post(cls, *args, **kwargs):
        try: 
            req = request.get_json()
            obj = cls.schema.load(req)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('post', obj, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def put(cls, *args, **kwargs): 
        try: 
            req = request.get_json()
            obj = cls.schema.load(req)
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('put', obj, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def patch(cls, id, *args, **kwargs): 
        try: 
            req = request.get_json()
            # get existing data 
            obj = cls.model.find_one(id, **cls.model_args)
            for attr, val in req.items(): 
                setattr(obj, attr, val)
            # save object to database 
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('patch', obj, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try:
            return cls.schema.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def delete(cls, id): 
        try: 
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('delete', obj, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            obj.delete()
            return {"status": "Deleted"}, 204
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400


class BaseCRUDResourceList(Resource):
    model: BaseModel
    schema: BaseSchema
    observable: BaseObservable = None
    model_args: dict = {}
    schema_args: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def get(cls, **kwargs):
        try: 
            objs = cls.model.find_all(**cls.model_args)
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('get', objs, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            if objs: 
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception as e:
            return [], 200
  
    @classmethod  
    def post(cls):
        try: 
            req = request.get_json()
            objs = cls.schema.load(req)
            cls.model.save_all_to_db(objs)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            _observable = getattr(cls, 'observable', None)
            if _observable:
                _observable.notify('post', objs, request)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try:
            return cls.schema.dump(objs), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
