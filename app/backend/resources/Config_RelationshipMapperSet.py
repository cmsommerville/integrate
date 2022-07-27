from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRelationshipMapperSet
from ..schemas import Schema_ConfigRelationshipMapperSet

class CRUD_ConfigRelationshipMapperSet(BaseCRUDResource): 
    model = Model_ConfigRelationshipMapperSet
    schema = Schema_ConfigRelationshipMapperSet

class CRUD_ConfigRelationshipMapperSet_List(BaseCRUDResourceList): 
    model = Model_ConfigRelationshipMapperSet
    schema = Schema_ConfigRelationshipMapperSet