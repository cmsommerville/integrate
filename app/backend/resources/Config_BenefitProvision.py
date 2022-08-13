from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitProvision
from ..schemas import Schema_ConfigBenefitProvision

class CRUD_ConfigBenefitProvision(BaseCRUDResource): 
    model = Model_ConfigBenefitProvision
    schema = Schema_ConfigBenefitProvision

class CRUD_ConfigBenefitProvision_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitProvision
    schema = Schema_ConfigBenefitProvision