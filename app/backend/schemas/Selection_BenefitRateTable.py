from app.extensions import ma
from app.shared import BaseSchema, PrimitiveField

from ..models import Model_SelectionBenefitRateTable


class Schema_SelectionBenefitRateTable(BaseSchema):
    class Meta:
        model = Model_SelectionBenefitRateTable
        load_instance = True
        include_relationships=True
        include_fk=True
