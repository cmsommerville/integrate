from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductMapperSet_Gender,  Model_ConfigProductMapperSet_SmokerStatus
from ..schemas import Schema_ConfigProductMapperSet_Gender, Schema_ConfigProductMapperSet_SmokerStatus

class CRUD_ConfigProductMapperSet_Gender(BaseCRUDResource): 
    model = Model_ConfigProductMapperSet_Gender
    schema = Schema_ConfigProductMapperSet_Gender()

class CRUD_ConfigProductMapperSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigProductMapperSet_Gender
    schema = Schema_ConfigProductMapperSet_Gender(many=True)

class CRUD_ConfigProductMapperSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigProductMapperSet_SmokerStatus
    schema = Schema_ConfigProductMapperSet_SmokerStatus()

class CRUD_ConfigProductMapperSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigProductMapperSet_SmokerStatus
    schema = Schema_ConfigProductMapperSet_SmokerStatus(many=True)



DISCRIMINATOR = {
    'gender': CRUD_ConfigProductMapperSet_Gender, 
    'smoker_status': CRUD_ConfigProductMapperSet_SmokerStatus, 
}

LIST_DISCRIMINATOR = {
    'gender': CRUD_ConfigProductMapperSet_Gender_List, 
    'smoker_status': CRUD_ConfigProductMapperSet_SmokerStatus_List, 
}

class CRUD_ConfigProductMapperSet(BaseCRUDResource):

    @classmethod
    def get(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.get(**kwargs)

    @classmethod
    def post(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.post(**kwargs)

    @classmethod
    def patch(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.patch(**kwargs)

    @classmethod
    def put(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.put(**kwargs)

    @classmethod
    def delete(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.delete(**kwargs)



class CRUD_ConfigProductMapperSet_List(BaseCRUDResource):

    @classmethod
    def get(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = LIST_DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.get(**kwargs)

    @classmethod
    def post(cls, config_attr_type_code: str, *args, **kwargs): 
        resource = LIST_DISCRIMINATOR.get(config_attr_type_code)
        if resource is None: 
            try: 
                return {"status": "error", "msg": f"Cannot find resource with config_attr_type_code: `${config_attr_type_code}`"}, 404
            except Exception as e: 
                return {"status": "error", "msg": str(e)}, 500
        return resource.post(**kwargs)
