from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitDurationSet
from ..schemas import Schema_ConfigBenefitDurationSet

class CRUD_ConfigBenefitDurationSet(BaseCRUDResource): 
    model = Model_ConfigBenefitDurationSet
    schema = Schema_ConfigBenefitDurationSet()

class CRUD_ConfigBenefitDurationSet_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitDurationSet
    schema = Schema_ConfigBenefitDurationSet(many=True)