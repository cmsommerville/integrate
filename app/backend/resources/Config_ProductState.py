from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductState
from ..schemas import Schema_ConfigProductState

class CRUD_ConfigProductState(BaseCRUDResource): 
    model = Model_ConfigProductState
    schema = Schema_ConfigProductState()

class CRUD_ConfigProductState_List(BaseCRUDResourceList): 
    model = Model_ConfigProductState
    schema = Schema_ConfigProductState(many=True)