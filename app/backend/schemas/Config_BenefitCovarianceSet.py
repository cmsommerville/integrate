from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigBenefitCovarianceSet, Model_ConfigBenefitCovarianceSet_ACL
from .Config_BenefitCovarianceDetail import Schema_ConfigBenefitCovarianceDetail


class Schema_ConfigBenefitCovarianceSet_ACL(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitCovarianceSet_ACL
        load_instance = True
        include_relationships=True
        include_fk=True

class Schema_ConfigBenefitCovarianceSet(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitCovarianceSet
        load_instance = True
        include_relationships=True
        include_fk=True

    acl = ma.Nested(Schema_ConfigBenefitCovarianceSet_ACL, many=True)
    covariance_details = ma.Nested(Schema_ConfigBenefitCovarianceDetail, many=True)
    optionality_code = ma.Function(lambda obj: obj.optionality.ref_attr_code, dump_only=True)
    optionality_label = ma.Function(lambda obj: obj.optionality.ref_attr_label, dump_only=True)