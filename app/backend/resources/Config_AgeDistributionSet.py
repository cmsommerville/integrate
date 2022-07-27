from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAgeDistributionSet
from ..schemas import Schema_ConfigAgeDistributionSet

class CRUD_ConfigAgeDistributionSet(BaseCRUDResource): 
    model = Model_ConfigAgeDistributionSet
    schema = Schema_ConfigAgeDistributionSet

class CRUD_ConfigAgeDistributionSet_List(BaseCRUDResourceList): 
    model = Model_ConfigAgeDistributionSet
    schema = Schema_ConfigAgeDistributionSet