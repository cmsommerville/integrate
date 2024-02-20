from app.shared import BaseSchema

from ..models import Model_SelectionBenefit


class Schema_SelectionBenefit(BaseSchema):
    class Meta:
        model = Model_SelectionBenefit
        load_instance = True
        include_relationships = True
        include_fk = True
