from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAgeMapperDetail
from ..schemas import Schema_ConfigAgeMapperDetail

class CRUD_ConfigAgeMapperDetail(BaseCRUDResource): 
    model = Model_ConfigAgeMapperDetail
    schema = Schema_ConfigAgeMapperDetail()

class CRUD_ConfigAgeMapperDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigAgeMapperDetail
    schema = Schema_ConfigAgeMapperDetail(many=True)