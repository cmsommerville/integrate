from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionCensusSet
from ..schemas import Schema_SelectionCensusSet

class CRUD_SelectionCensusSet(BaseCRUDResource): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet

class CRUD_SelectionCensusSet_List(BaseCRUDResourceList): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet