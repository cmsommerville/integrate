from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigFactorSet
from ..schemas import Schema_ConfigFactorSet


class CRUD_ConfigFactorSet(BaseCRUDResource):
    model = Model_ConfigFactorSet
    schema = Schema_ConfigFactorSet()


class CRUD_ConfigFactorSet_List(BaseCRUDResourceList):
    model = Model_ConfigFactorSet
    schema = Schema_ConfigFactorSet(many=True)
