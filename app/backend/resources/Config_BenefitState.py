from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitState
from ..schemas import Schema_ConfigBenefitState

class CRUD_ConfigBenefitState(BaseCRUDResource): 
    model = Model_ConfigBenefitState
    schema = Schema_ConfigBenefitState

class CRUD_ConfigBenefitState_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitState
    schema = Schema_ConfigBenefitState