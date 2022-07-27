from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvisionState
from ..schemas import Schema_ConfigProvisionState

class CRUD_ConfigProvisionState(BaseCRUDResource): 
    model = Model_ConfigProvisionState
    schema = Schema_ConfigProvisionState

class CRUD_ConfigProvisionState_List(BaseCRUDResourceList): 
    model = Model_ConfigProvisionState
    schema = Schema_ConfigProvisionState