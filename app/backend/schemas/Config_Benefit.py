from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefit
# from .Ref_Master import Schema_RefBenefit

class Schema_ConfigBenefit(BaseSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships=True
        include_fk=True

    # ref_benefit = ma.Nested(Schema_RefBenefit)