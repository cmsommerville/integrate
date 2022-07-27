from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvision
from ..schemas import Schema_ConfigProvision

class CRUD_ConfigProvision(BaseCRUDResource): 
    model = Model_ConfigProvision
    schema = Schema_ConfigProvision

class CRUD_ConfigProvision_List(BaseCRUDResourceList): 
    model = Model_ConfigProvision
    schema = Schema_ConfigProvision