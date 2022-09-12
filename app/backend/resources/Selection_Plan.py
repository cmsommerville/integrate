from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionPlan
from ..schemas import Schema_SelectionPlan

class CRUD_SelectionPlan(BaseCRUDResource): 
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan

class CRUD_SelectionPlan_List(BaseCRUDResourceList): 
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan

class Test_SelectionPlan(Resource): 
    
    @classmethod
    def get(cls, id: int):
        data = Model_SelectionPlan.get_rate_table_factors(id)
        print(data[0])
        return {"hello": "world"}, 200
