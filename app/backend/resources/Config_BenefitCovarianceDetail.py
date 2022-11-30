from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitCovarianceDetail
from ..schemas import Schema_ConfigBenefitCovarianceDetail

class CRUD_ConfigBenefitCovarianceDetail(BaseCRUDResource): 
    model = Model_ConfigBenefitCovarianceDetail
    schema = Schema_ConfigBenefitCovarianceDetail()

class CRUD_ConfigBenefitCovarianceDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigBenefitCovarianceDetail
    schema = Schema_ConfigBenefitCovarianceDetail(many=True)