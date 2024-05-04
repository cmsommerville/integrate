from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_AuthUserRole

class Schema_AuthUserRole_JWT(BaseSchema):
    auth_role_code = ma.Function(lambda obj: obj.role.auth_role_code)

class Schema_AuthUserRole(BaseSchema):
    class Meta:
        model = Model_AuthUserRole
        load_instance = True
        include_fk = True
        include_relationships = True

    auth_role_code = ma.Function(lambda obj: obj.role.auth_role_code)