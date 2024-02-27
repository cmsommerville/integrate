from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionBenefit
from ..schemas import Schema_SelectionBenefit


class CRUD_SelectionBenefit(BaseSelectionCRUDResource):
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit()
    EVENT = "selection_benefit"


class CRUD_SelectionBenefit_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionBenefit
    schema = Schema_SelectionBenefit(many=True)
    EVENT = "selection_benefit"
