from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionPlan
from ..schemas import Schema_SelectionPlan


class CRUD_SelectionPlan(BaseCRUDResource):
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan()


class CRUD_SelectionPlan_List(BaseCRUDResourceList):
    model = Model_SelectionPlan
    schema = Schema_SelectionPlan(many=True)
