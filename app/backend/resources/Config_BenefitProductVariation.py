from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitProductVariation
from ..schemas import Schema_ConfigBenefitProductVariation

class CRUD_ConfigBenefitProductVariation(BaseCRUDResource): 
    model = Model_ConfigBenefitProductVariation
    schema = Schema_ConfigBenefitProductVariation()

class CRUD_ConfigBenefitProductVariation_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitProductVariation
    schema = Schema_ConfigBenefitProductVariation(many=True)