from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefit, Model_ConfigBenefitAuthority
# from .Ref_Master import Schema_RefBenefit

class Schema_ConfigBenefitAuthority(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitAuthority
        load_instance = True
        include_relationships=True
        include_fk=True

class Schema_ConfigBenefit(BaseSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships=True
        include_fk=True

    user_access_level = ma.Integer(dump_only=True)
    min_value = ma.Float(dump_only=True)
    max_value = ma.Float(dump_only=True)
    step_value = ma.Float(dump_only=True)
    default_value = ma.Float(dump_only=True)
    benefit_authority = ma.Nested(Schema_ConfigBenefitAuthority, many=True, load_only=True)
    # ref_benefit = ma.Nested(Schema_RefBenefit)