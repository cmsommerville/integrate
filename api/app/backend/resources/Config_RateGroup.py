from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRateGroup
from ..schemas import Schema_ConfigRateGroup

class CRUD_ConfigRateGroup(BaseCRUDResource): 
    model = Model_ConfigRateGroup
    schema = Schema_ConfigRateGroup()

class CRUD_ConfigRateGroup_List(BaseCRUDResourceList): 
    model = Model_ConfigRateGroup
    schema = Schema_ConfigRateGroup(many=True)