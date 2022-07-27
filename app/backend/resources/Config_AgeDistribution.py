from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAgeDistribution
from ..schemas import Schema_ConfigAgeDistribution

class CRUD_ConfigAgeDistribution(BaseCRUDResource): 
    model = Model_ConfigAgeDistribution
    schema = Schema_ConfigAgeDistribution

class CRUD_ConfigAgeDistribution_List(BaseCRUDResourceList): 
    model = Model_ConfigAgeDistribution
    schema = Schema_ConfigAgeDistribution