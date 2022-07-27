from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAttributeDetail
from ..schemas import Schema_ConfigAttributeDetail

class CRUD_ConfigAttributeDetail(BaseCRUDResource): 
    model = Model_ConfigAttributeDetail
    schema = Schema_ConfigAttributeDetail

class CRUD_ConfigAttributeDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDetail
    schema = Schema_ConfigAttributeDetail