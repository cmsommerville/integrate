from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionBenefitDuration
from ..schemas import Schema_SelectionBenefitDuration

class CRUD_SelectionBenefitDuration(BaseCRUDResource): 
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration

class CRUD_SelectionBenefitDuration_List(BaseCRUDResourceList): 
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration