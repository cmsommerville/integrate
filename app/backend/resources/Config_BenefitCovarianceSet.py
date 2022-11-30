from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitCovarianceSet
from ..schemas import Schema_ConfigBenefitCovarianceSet

class CRUD_ConfigBenefitCovarianceSet(BaseCRUDResource): 
    model = Model_ConfigBenefitCovarianceSet
    schema = Schema_ConfigBenefitCovarianceSet()

class CRUD_ConfigBenefitCovarianceSet_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitCovarianceSet
    schema = Schema_ConfigBenefitCovarianceSet(many=True)