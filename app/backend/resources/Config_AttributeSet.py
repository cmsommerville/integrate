from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList, BaseObservable
from ..models import Model_ConfigAttributeSet_Gender, Model_ConfigAttributeSet_SmokerStatus, Model_ConfigAttributeSet_Relationship, Model_ConfigAttributeSet, Model_ConfigAttributeSet_NoJoin
from ..schemas import Schema_ConfigAttributeSet_Gender, Schema_ConfigAttributeSet_SmokerStatus,  Schema_ConfigAttributeSet_Relationship, Schema_ConfigAttributeSet, Schema_ConfigAttributeSet_NoJoin


class CRUD_ConfigAttributeSet_Gender(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender()

class CRUD_ConfigAttributeSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender(many=True)

class CRUD_ConfigAttributeSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus()

class CRUD_ConfigAttributeSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus(many=True)

class CRUD_ConfigAttributeSet_Relationship(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Relationship()

class CRUD_ConfigAttributeSet_Relationship_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Relationship(many=True)

class CRUD_ConfigAttributeSet_NoJoin(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_NoJoin
    schema = Schema_ConfigAttributeSet_NoJoin()

class CRUD_ConfigAttributeSet_NoJoin_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_NoJoin
    schema = Schema_ConfigAttributeSet_NoJoin(many=True)





DISCRIMINATOR = {
    'gender': CRUD_ConfigAttributeSet_Gender, 
    'smoker_status': CRUD_ConfigAttributeSet_SmokerStatus, 
    'relationship': CRUD_ConfigAttributeSet_Relationship, 
    '__nojoin__': CRUD_ConfigAttributeSet_NoJoin, 
}

LIST_DISCRIMINATOR = {
    'gender': CRUD_ConfigAttributeSet_Gender_List, 
    'smoker_status': CRUD_ConfigAttributeSet_SmokerStatus_List, 
    'relationship': CRUD_ConfigAttributeSet_Relationship_List, 
    '__nojoin__': CRUD_ConfigAttributeSet_NoJoin_List, 
}

class CRUD_ConfigAttributeSet(BaseCRUDResource):

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



class CRUD_ConfigAttributeSet_List(BaseCRUDResource):

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
