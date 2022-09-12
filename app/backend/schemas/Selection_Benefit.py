from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionBenefit
from .Config_Benefit import Schema_ConfigBenefit

class Schema_SelectionBenefit(BaseSchema):
    class Meta:
        model = Model_SelectionBenefit
        load_instance = True
        include_relationships=True
        include_fk=True

    config_benefit = ma.Nested(Schema_ConfigBenefit)