from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitCovarianceDetail


class Schema_ConfigBenefitCovarianceDetail(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitCovarianceDetail
        load_instance = True
        include_relationships=True
        include_fk=True