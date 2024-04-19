from app.extensions import ma
from app.shared import BaseSchema

from ..models import (
    Model_ConfigBenefitDurationDetail,
    Model_ConfigBenefitDurationDetailAuth_ACL,
)


class Schema_ConfigBenefitDurationDetail_ACL(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationDetailAuth_ACL
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_ConfigBenefitDurationDetail(BaseSchema):
    class Meta:
        model = Model_ConfigBenefitDurationDetail
        load_instance = True
        include_relationships = True
        include_fk = True
        load_only = ("acl",)
