from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefitVariation
from ..schemas import Schema_ConfigBenefitVariation


class CRUD_ConfigBenefitVariation(BaseCRUDResource):
    model = Model_ConfigBenefitVariation
    schema = Schema_ConfigBenefitVariation()


class CRUD_ConfigBenefitVariation_List(BaseCRUDResourceList):
    model = Model_ConfigBenefitVariation
    schema = Schema_ConfigBenefitVariation(many=True)
