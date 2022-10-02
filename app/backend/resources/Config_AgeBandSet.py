from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAgeBandSet
from ..schemas import Schema_ConfigAgeBandSet

class CRUD_ConfigAgeBandSet(BaseCRUDResource): 
    model = Model_ConfigAgeBandSet
    schema = Schema_ConfigAgeBandSet()

class CRUD_ConfigAgeBandSet_List(BaseCRUDResourceList): 
    model = Model_ConfigAgeBandSet
    schema = Schema_ConfigAgeBandSet(many=True)