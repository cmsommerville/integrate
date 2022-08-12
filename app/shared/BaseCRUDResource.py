from flask import request
from flask_restx import Resource
from .BaseModel import BaseModel
from .BaseSchema import BaseSchema
from .BaseObservable import BaseObservable

class BaseCRUDResource(Resource):
    model: BaseModel
    schema: BaseSchema
    observable: BaseObservable = None

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def get(cls, id, *args, **kwargs):
        schema_instance = cls.schema()
        try: 
            obj = cls.model.find_one(id)
            if obj: 
                return schema_instance.dump(obj), 200
            raise Exception(f"No data found for id {id}")
        except Exception as e:
            return {}, 200
  
    @classmethod  
    def post(cls, *args, **kwargs):
        schema_instance = cls.schema()
        try: 
            req = request.get_json()
            obj = schema_instance.load(req)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            return schema_instance.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def put(cls, *args, **kwargs): 
        schema_instance = cls.schema()
        try: 
            req = request.get_json()
            obj = schema_instance.load(req)
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try: 
            return schema_instance.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def patch(cls, id, *args, **kwargs): 
        schema_instance = cls.schema()
        try: 
            req = request.get_json()
            # get existing data 
            orig_obj = cls.model.find_one(id)
            # dump existing data to json 
            data = schema_instance.dump(orig_obj)
            # add the modified data and load to object
            obj = schema_instance.load({**data, **req})
            # save object to database 
            obj.save_to_db()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        
        try:
            return schema_instance.dump(obj), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @classmethod
    def delete(cls, id): 
        try: 
            obj = cls.model.find_one(id)
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

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def get(cls, **kwargs):
        try: 
            objs = cls.model.find_all(**kwargs)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            if objs: 
                return cls.schema(many=True).dump(objs), 200
            raise Exception("No data found")
        except Exception as e:
            return [], 200
  
    @classmethod  
    def post(cls):
        try: 
            schema_list_instance = cls.schema(many=True)
            req = request.get_json()
            objs = schema_list_instance.load(req)
            cls.model.save_all_to_db(objs)
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try:
            return schema_list_instance.dump(objs), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
