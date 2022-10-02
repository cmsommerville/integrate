from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductVariation
from ..schemas import Schema_ConfigProductVariation

class CRUD_ConfigProductVariation(BaseCRUDResource): 
    model = Model_ConfigProductVariation
    schema = Schema_ConfigProductVariation()

class CRUD_ConfigProductVariation_List(BaseCRUDResourceList): 
    model = Model_ConfigProductVariation
    schema = Schema_ConfigProductVariation(many=True)