from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionBenefit
from ..schemas import Schema_SelectionBenefit

class CRUD_SelectionBenefit(BaseCRUDResource): 
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit

class CRUD_SelectionBenefit_List(BaseCRUDResourceList): 
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit