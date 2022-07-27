from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigFactorRule
from ..schemas import Schema_ConfigFactorRule

class CRUD_ConfigFactorRule(BaseCRUDResource): 
    model = Model_ConfigFactorRule
    schema = Schema_ConfigFactorRule

class CRUD_ConfigFactorRule_List(BaseCRUDResourceList): 
    model = Model_ConfigFactorRule
    schema = Schema_ConfigFactorRule