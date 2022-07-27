from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductMapperDetail
from ..schemas import Schema_ConfigProductMapperDetail

class CRUD_ConfigProductMapperDetail(BaseCRUDResource): 
    model = Model_ConfigProductMapperDetail
    schema = Schema_ConfigProductMapperDetail

class CRUD_ConfigProductMapperDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigProductMapperDetail
    schema = Schema_ConfigProductMapperDetail