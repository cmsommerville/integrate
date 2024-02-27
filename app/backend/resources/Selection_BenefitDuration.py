from app.shared import BaseSelectionCRUDResource, BaseSelectionCRUDResourceList
from ..models import Model_SelectionBenefitDuration
from ..schemas import Schema_SelectionBenefitDuration


class CRUD_SelectionBenefitDuration(BaseSelectionCRUDResource):
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration()
    EVENT = "selection_benefit_duration"


class CRUD_SelectionBenefitDuration_List(BaseSelectionCRUDResourceList):
    model = Model_SelectionBenefitDuration
    schema = Schema_SelectionBenefitDuration(many=True)
    EVENT = "selection_benefit_duration"
