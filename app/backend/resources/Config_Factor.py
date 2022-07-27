from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigFactor
from ..schemas import Schema_ConfigFactor

class CRUD_ConfigFactor(BaseCRUDResource): 
    model = Model_ConfigFactor
    schema = Schema_ConfigFactor

class CRUD_ConfigFactor_List(BaseCRUDResourceList): 
    model = Model_ConfigFactor
    schema = Schema_ConfigFactor