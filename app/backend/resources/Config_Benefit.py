from marshmallow import EXCLUDE
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigBenefit
from ..schemas import Schema_ConfigBenefit_CRUD, Schema_ConfigBenefit_Data


class CRUD_ConfigBenefit(BaseCRUDResource):
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_CRUD(unknown=EXCLUDE)


class CRUD_ConfigBenefit_List(BaseCRUDResourceList):
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_CRUD(many=True, unknown=EXCLUDE)


class Data_ConfigBenefit(BaseCRUDResource):
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_Data()


class Data_ConfigBenefit_List(BaseCRUDResourceList):
    model = Model_ConfigBenefit
    schema = Schema_ConfigBenefit_Data(many=True)
