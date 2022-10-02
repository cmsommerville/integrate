from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit

class CRUD_ConfigBenefit(BaseCRUDResource): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit()

class CRUD_ConfigBenefit_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit(many=True)