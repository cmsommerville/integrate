from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_AuthUser
from .AuthUserRole import Schema_AuthUserRole


class Schema_AuthUser_Output(BaseSchema):
    auth_user_id = ma.Integer()
    user_name = ma.String()
    first_name = ma.String()
    last_name = ma.String()
    email_address = ma.String()
    avatar = ma.String()
    roles = ma.Function(lambda obj: [r.role.auth_role_code for r in obj.roles])
    permissions = ma.Method("get_permissions")
    direct_reports = ma.Method("get_direct_reports")

    def get_permissions(self, obj):
        permissions = []
        for role in obj.roles:
            permissions.extend(
                [p.permission.auth_permission_code for p in role.role.permissions]
            )
        return permissions

    def get_direct_reports(self, obj):
        return [dr.user_name for dr in obj.get_direct_reports()]


class Schema_NewUser(ma.Schema):
    user_name = ma.String()
    password = ma.String(load_only=True)
    first_name = ma.String()
    last_name = ma.String()
    email_address = ma.String()
    avatar = ma.String(required=False)
    roles = ma.List(ma.String(), required=False)
    user_type_code = ma.Constant("app_managed_user")


class Schema_AuthUser(BaseSchema):
    class Meta:
        model = Model_AuthUser
        load_instance = True
        include_fk = True
        include_relationships = True

    auth_user_id = ma.Integer()
    user_name = ma.String()
    hashed_password = ma.Raw(load_only=True)
    first_name = ma.String()
    last_name = ma.String()
    email_address = ma.String()
    avatar = ma.String()
    password_last_changed_dt = ma.DateTime(load_only=True)

    roles = ma.Nested(Schema_AuthUserRole, many=True)
