from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionProvision
from ..schemas import Schema_SelectionProvision

class CRUD_SelectionProvision(BaseCRUDResource): 
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision

class CRUD_SelectionProvision_List(BaseCRUDResourceList): 
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision