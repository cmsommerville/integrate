from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_RefStates
from ..schemas import Schema_RefStates

class CRUD_RefStates(BaseCRUDResource): 
    model = Model_RefStates
    schema = Schema_RefStates()

class CRUD_RefStates_List(BaseCRUDResourceList): 
    model = Model_RefStates
    schema = Schema_RefStates(many=True)