from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionPlan, Model_ConfigProduct, \
    Model_ConfigProductMapperSet_Gender, Model_ConfigProductMapperSet_SmokerStatus

from ..schemas import Schema_SelectionPlan, Schema_ConfigProduct, \
    Schema_ConfigProductMapperSet_Gender, Schema_ConfigProductMapperSet_SmokerStatus

class CRUD_SelectionPlan(BaseCRUDResource): 
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan()


class CRUD_SelectionPlan_List(BaseCRUDResourceList): 
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan(many=True)



class Resource_SelectionPlan_ConfigProduct(Resource):
    """
    Get the product configuration for the selected plan
    """

    @classmethod
    def get(cls, id): 
        try: 
            schema = Schema_ConfigProduct()
            plan = Model_SelectionPlan.find_one(id)
            product  = Model_ConfigProduct.find_one(plan.config_product_id)
            return schema.dump(product)
        except Exception as e: 
            return {"status": "error", "msg": str(e)}, 400


class Resource_SelectionPlan_GenderProductMapper(Resource):
    """
    Get the gender product mappers for the selected plan
    """

    @classmethod
    def get(cls, id): 
        try: 
            schema = Schema_ConfigProductMapperSet_Gender(many=True, exclude=('mappers',))
            plan = Model_SelectionPlan.find_one(id)
            mapper  = Model_ConfigProductMapperSet_Gender.find_by_product(plan.config_product_id)
            return schema.dump(mapper)
        except Exception as e: 
            return {"status": "error", "msg": str(e)}, 400


class Resource_SelectionPlan_SmokerStatusProductMapper(Resource):
    """
    Get the smoker status product mappers for the selected plan
    """

    @classmethod
    def get(cls, id): 
        try: 
            schema = Schema_ConfigProductMapperSet_SmokerStatus(many=True, exclude=('mappers',))
            plan = Model_SelectionPlan.find_one(id)
            mapper  = Model_ConfigProductMapperSet_SmokerStatus.find_by_product(plan.config_product_id)
            return schema.dump(mapper)
        except Exception as e: 
            return {"status": "error", "msg": str(e)}, 400