from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionCoverage
from ..schemas import Schema_SelectionCoverage


class CRUD_SelectionCoverage(BaseSelectionCRUDResource):
    model = Model_SelectionCoverage
    schema = Schema_SelectionCoverage()
    EVENT = "selection_coverage"


class CRUD_SelectionCoverage_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionCoverage
    schema = Schema_SelectionCoverage(many=True)
    EVENT = "selection_coverage"

    @classmethod
    def bulk_create(cls, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
