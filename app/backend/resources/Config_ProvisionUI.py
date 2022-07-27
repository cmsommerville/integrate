from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvisionUI
from ..schemas import Schema_ConfigProvisionUI

class CRUD_ConfigProvisionUI(BaseCRUDResource): 
    model = Model_ConfigProvisionUI
    schema = Schema_ConfigProvisionUI

class CRUD_ConfigProvisionUI_List(BaseCRUDResourceList): 
    model = Model_ConfigProvisionUI
    schema = Schema_ConfigProvisionUI