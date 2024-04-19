from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionCoverage
from .Selection_Benefit import Schema_SelectionBenefit


class Schema_SelectionCoverage(BaseSchema):
    class Meta:
        model = Model_SelectionCoverage
        load_instance = True
        include_fk = True

    benefits = ma.Nested("Schema_SelectionBenefit", many=True)
    # benefits = ma.Method("get_benefits", deserialize="load_benefits")

    def get_benefits(self, obj, *args, **kwargs):
        return Schema_SelectionBenefit(context=self.context).dump(
            obj.get_benefits(**self.context), many=True
        )

    def load_benefits(self, value, *args, **kwargs):
        return [Schema_SelectionBenefit(context=self.context).load(v) for v in value]
