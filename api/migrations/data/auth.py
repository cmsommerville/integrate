import os
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
        "auth_permission_code": "read:selection:all",
        "auth_permission_description": "Read permissions to selection RPC modules for all plans",
    },
    {
        "auth_permission_code": "read:selection:hierarchy",
        "auth_permission_description": "Read permissions to selection RPC modules for plans belonging to the user and her direct reports",
    },
    {
        "auth_permission_code": "read:selection:self",
        "auth_permission_description": "Read permissions to selection RPC modules for plans belonging to the user",
    },
    {
        "auth_permission_code": "write:selection:all",
        "auth_permission_description": "Write/edit permissions to selection RPC modules for all plans",
    },
    {
        "auth_permission_code": "write:selection:hierarchy",
        "auth_permission_description": "Write/edit permissions to selection RPC modules for plans belonging to the user and her direct reports",
    },
    {
        "auth_permission_code": "write:selection:self",
        "auth_permission_description": "Write/edit permissions to selection RPC modules for plans belonging to the user",
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
    data = {
        "user_type_code": "app_managed_user",
        "user_name": "sys",
        "first_name": "System",
        "last_name": "Admin",
        "email_address": os.getenv("SYS_SUPERUSER_EMAIL_ADDRESS", "sys@dummy.com"),
        "roles": ["superuser"],
        "password": pwd,
    }
    return register_user(data)
