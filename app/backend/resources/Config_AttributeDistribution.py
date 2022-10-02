from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAttributeDistribution
from ..schemas import Schema_ConfigAttributeDistribution

class CRUD_ConfigAttributeDistribution(BaseCRUDResource): 
    model = Model_ConfigAttributeDistribution
    schema = Schema_ConfigAttributeDistribution()

class CRUD_ConfigAttributeDistribution_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDistribution
    schema = Schema_ConfigAttributeDistribution(many=True)