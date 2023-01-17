from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefit, Model_ConfigBenefitAuth, Model_ConfigBenefitAuth_ACL
from .Ref_Master import Schema_RefBenefit, Schema_RefUnitCode

class Schema_ConfigBenefitAuth_ACL(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitAuth_ACL
        load_instance = True
        include_relationships=True
        include_fk=True

class Schema_ConfigBenefitAuth(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitAuth
        load_instance = True
        include_relationships=True
        include_fk=True
    
    acl = ma.Nested(Schema_ConfigBenefitAuth_ACL, many=True)

class Schema_ConfigBenefit_CRUD(BaseSchema):
    class Meta: 
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships=True
        include_fk=True
    
    benefit_auth = ma.Nested(Schema_ConfigBenefitAuth, many=True)
    ref_benefit = ma.Nested(Schema_RefBenefit, dump_only=True)
    unit_type = ma.Nested(Schema_RefUnitCode, dump_only=True)


class Schema_ConfigBenefit_Data(BaseSchema):
    class Meta:
        model = Model_ConfigBenefit
        load_instance = True
        include_relationships=True
        include_fk=True

    priority = ma.Integer(dump_only=True)
    min_value = ma.Float(dump_only=True)
    max_value = ma.Float(dump_only=True)
    step_value = ma.Float(dump_only=True)
    default_value = ma.Float(dump_only=True)
    benefit_auth = ma.Nested(Schema_ConfigBenefitAuth, many=True, load_only=True)
    ref_benefit = ma.Nested(Schema_RefBenefit)
    unit_type = ma.Nested(Schema_RefUnitCode)