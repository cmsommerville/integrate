from app.auth.auth import register_user
from app.extensions import db
from app.auth.models import (
    Model_AuthRole,
    Model_AuthPermission,
    Model_AuthRolePermission,
)

SUPERUSER_ROLE = {
    "auth_role_code": "superuser",
    "auth_role_label": "Super User with all permissions",
}


AUTH_PERMISSIONS = [
    {
        "auth_permission_code": "admin",
        "auth_permission_description": "Admin permissions",
    },
    {
        "auth_permission_code": "read:config_product",
        "auth_permission_description": "Reader permissions to product configurator",
    },
    {
        "auth_permission_code": "write:config_product",
        "auth_permission_description": "Writer permissions to product configurator",
    },
    {
        "auth_permission_code": "read:config_benefit",
        "auth_permission_description": "Reader permissions to benefit configurator",
    },
    {
        "auth_permission_code": "write:config_benefit",
        "auth_permission_description": "Writer permissions to benefit configurator",
    },
    {
        "auth_permission_code": "read:config_provision",
        "auth_permission_description": "Reader permissions to provision configurator",
    },
    {
        "auth_permission_code": "write:config_provision",
        "auth_permission_description": "Writer permissions to provision configurator",
    },
    {
        "auth_permission_code": "read:selection",
        "auth_permission_description": "Read permissions to selection RPC modeules",
    },
    {
        "auth_permission_code": "write:selection",
        "auth_permission_description": "Write/edit permissions to selection RPC modules",
    },
]


def register_superuser_roles_permissions():
    permissions = [
        Model_AuthPermission(**permission) for permission in AUTH_PERMISSIONS
    ]
    db.session.add_all(permissions)

    role = Model_AuthRole(**SUPERUSER_ROLE)
    db.session.add(role)
    db.session.flush()

    role.permissions = [
        Model_AuthRolePermission(
            auth_permission_id=p.auth_permission_id, auth_role_id=role.auth_role_id
        )
        for p in permissions
    ]
    db.session.add(role)
    db.session.commit()
    return role


def register_sys_admin(pwd):
    return register_user("sys", pwd, ["superuser"])
