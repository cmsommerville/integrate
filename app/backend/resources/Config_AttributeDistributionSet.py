from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAttributeDistributionSet_Gender, Model_ConfigAttributeDistributionSet_SmokerStatus
from ..schemas import Schema_ConfigAttributeDistributionSet_Gender, Schema_ConfigAttributeDistributionSet_SmokerStatus



class CRUD_ConfigAttributeDistributionSet_Gender(BaseCRUDResource): 
    model = Model_ConfigAttributeDistributionSet_Gender
    schema = Schema_ConfigAttributeDistributionSet_Gender()

class CRUD_ConfigAttributeDistributionSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDistributionSet_Gender
    schema = Schema_ConfigAttributeDistributionSet_Gender(many=True)

class CRUD_ConfigAttributeDistributionSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigAttributeDistributionSet_SmokerStatus
    schema = Schema_ConfigAttributeDistributionSet_SmokerStatus()

class CRUD_ConfigAttributeDistributionSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDistributionSet_SmokerStatus
    schema = Schema_ConfigAttributeDistributionSet_SmokerStatus(many=True)




DISCRIMINATOR = {
    'gender': CRUD_ConfigAttributeDistributionSet_Gender, 
    'smoker_status': CRUD_ConfigAttributeDistributionSet_SmokerStatus
}

LIST_DISCRIMINATOR = {
    'gender': CRUD_ConfigAttributeDistributionSet_Gender_List, 
    'smoker_status': CRUD_ConfigAttributeDistributionSet_SmokerStatus_List
}

class CRUD_ConfigAttributeDistributionSet(BaseCRUDResource):

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



class CRUD_ConfigAttributeDistributionSet_List(BaseCRUDResource):

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
