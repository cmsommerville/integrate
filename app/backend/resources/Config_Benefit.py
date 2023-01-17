from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit_CRUD, Schema_ConfigBenefit_Data

class CRUD_ConfigBenefit(BaseCRUDResource): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_CRUD()

class CRUD_ConfigBenefit_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_CRUD(many=True)

class Data_ConfigBenefit(BaseCRUDResource): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_Data()

class Data_ConfigBenefit_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_Data(many=True)

