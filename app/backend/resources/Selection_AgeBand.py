from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionAgeBand
from ..schemas import Schema_SelectionAgeBand

class CRUD_SelectionAgeBand(BaseCRUDResource): 
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand

class CRUD_SelectionAgeBand_List(BaseCRUDResourceList): 
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand