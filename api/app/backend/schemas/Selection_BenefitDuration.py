from app.shared import BaseSchema

from ..models import Model_SelectionBenefitDuration


class Schema_SelectionBenefitDuration(BaseSchema):
    class Meta:
        model = Model_SelectionBenefitDuration
        load_instance = True
        include_relationships = True
        include_fk = True
