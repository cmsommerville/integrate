from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigCoverage
from ..schemas import Schema_ConfigCoverage

class CRUD_ConfigCoverage(BaseCRUDResource): 
    model = Model_ConfigCoverage
    schema = Schema_ConfigCoverage()

class CRUD_ConfigCoverage_List(BaseCRUDResourceList): 
    model = Model_ConfigCoverage
    schema = Schema_ConfigCoverage(many=True)