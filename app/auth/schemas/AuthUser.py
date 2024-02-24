from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_AuthUser
from .AuthUserRole import Schema_AuthUserRole


class Schema_AuthUser_Output(BaseSchema):
    auth_user_id = ma.Integer()
    user_name = ma.String()
    roles = ma.Function(lambda obj: [r.role.auth_role_code for r in obj.roles])
    permissions = ma.Method("get_permissions")

    def get_permissions(self, obj):
        permissions = []
        for role in obj.roles:
            permissions.extend(
                [p.permission.auth_permission_code for p in role.role.permissions]
            )
        return permissions


class Schema_AuthUser(BaseSchema):
    class Meta:
        model = Model_AuthUser
        load_instance = True
        include_fk = True
        include_relationships = True

    auth_user_id = ma.Integer()
    user_name = ma.String()
    hashed_password = ma.Raw(load_only=True)

    roles = ma.Nested(Schema_AuthUserRole, many=True)
