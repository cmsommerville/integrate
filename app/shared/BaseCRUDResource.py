from flask import request
from flask_restx import Resource
from .BaseModel import BaseModel
from .BaseSchema import BaseSchema
from app.auth import authorize, ResourcePermissions

class BaseCRUDResource(Resource):
    model: BaseModel
    schema: BaseSchema
    model_args: dict = {}
    permissions = ResourcePermissions()

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    @authorize()
    def get(cls, id, *args, **kwargs):
        try: 
            obj = cls.model.find_one(id, **cls.model_args)
        except Exception as e:
            return {}, 200

        return cls.schema.dump(obj), 200
  
    @classmethod  
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
    permissions = ResourcePermissions()

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    @authorize()
    def get(cls, *args, **kwargs):
        try: 
            objs = cls.model.find_all(**cls.model_args)
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try: 
            if objs: 
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception as e:
            return [], 200
  
    @classmethod  
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
