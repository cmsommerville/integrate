from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitDurationDetail
from ..schemas import Schema_ConfigBenefitDurationDetail

class CRUD_ConfigBenefitDurationDetail(BaseCRUDResource): 
    model = Model_ConfigBenefitDurationDetail
    schema = Schema_ConfigBenefitDurationDetail

class CRUD_ConfigBenefitDurationDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitDurationDetail
    schema = Schema_ConfigBenefitDurationDetail