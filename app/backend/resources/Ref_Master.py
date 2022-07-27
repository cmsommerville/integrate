from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_RefBenefit
from ..schemas import Schema_RefBenefit

class Resource_RefBenefit(BaseCRUDResource): 
    model = Model_RefBenefit
    schema = Schema_RefBenefit

class Resource_RefBenefit_List(BaseCRUDResourceList): 
    model = Model_RefBenefit
    schema = Schema_RefBenefit