from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRelationshipMapperDetail
from ..schemas import Schema_ConfigRelationshipMapperDetail

class CRUD_ConfigRelationshipMapperDetail(BaseCRUDResource): 
    model = Model_ConfigRelationshipMapperDetail
    schema = Schema_ConfigRelationshipMapperDetail()

class CRUD_ConfigRelationshipMapperDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigRelationshipMapperDetail
    schema = Schema_ConfigRelationshipMapperDetail(many=True)