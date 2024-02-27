from app.shared import BaseSelectionCRUDResourceList, BaseSelectionCRUDResource
from ..models import Model_SelectionAgeBand
from ..schemas import Schema_SelectionAgeBand


class CRUD_SelectionAgeBand(BaseSelectionCRUDResource):
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand()
    EVENT = "selection_age_band"


class CRUD_SelectionAgeBand_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionAgeBand
    schema = Schema_SelectionAgeBand(many=True)
    EVENT = "selection_age_band"
