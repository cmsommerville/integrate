from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionCensusDetail
from ..schemas import Schema_SelectionCensusDetail

class CRUD_SelectionCensusDetail(BaseCRUDResource): 
    model = Model_SelectionCensusDetail
    schema = Schema_SelectionCensusDetail

class CRUD_SelectionCensusDetail_List(BaseCRUDResourceList): 
    model = Model_SelectionCensusDetail
    schema = Schema_SelectionCensusDetail