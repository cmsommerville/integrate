from app.shared import BaseSchema

from ..models import Model_SelectionBenefitRate


class Schema_SelectionBenefitRate(BaseSchema):
    class Meta:
        model = Model_SelectionBenefitRate
        load_instance = True
        include_relationships = True
        include_fk = True
