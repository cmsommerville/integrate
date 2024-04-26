import os
import requests
from requests.compat import urljoin

ROLES = [
    {
        "auth_role_code": "superuser",
        "auth_role_label": "Super User",
    }
]

PERMISSIONS = [
    {
        "auth_permission_code": "read:config_product",
        "auth_permission_description": "Reader permissions to product configurator",
    },
    {
        "auth_permission_code": "write:config_product",
        "auth_permission_description": "Writer permissions to product configurator",
    },
    {
        "auth_permission_code": "delete:config_product",
        "auth_permission_description": "Delete permissions to product configurator",
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
        "auth_permission_code": "delete:config_benefit",
        "auth_permission_description": "Delete permissions to benefit configurator",
    },
    {
        "auth_permission_code": "read:selection",
        "auth_permission_description": "Read permissions to selection",
    },
    {
        "auth_permission_code": "write:selection",
        "auth_permission_description": "Write/edit permissions to selection RPC modules",
    },
    {
        "auth_permission_code": "delete:selection",
        "auth_permission_description": "Delete permissions to selection RPC modules",
    },
]


def load_roles(hostname, **kwargs):
    url = urljoin(hostname, "api/auth/roles")
    res = requests.post(url, json=ROLES, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    return res.json()


def load_permissions(hostname, **kwargs):
    url = urljoin(hostname, "api/auth/permissions")
    res = requests.post(url, json=PERMISSIONS, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    return res.json()


def assign_perms_to_superuser(hostname, role_id, permission_code_list, **kwargs):
    url = urljoin(hostname, f"api/auth/role/{role_id}/permissions")
    res = requests.post(url, json={"permissions": permission_code_list}, **kwargs)
    if not res.ok:
        raise Exception(res.text)
    return res.json()


SYS_USER_NAME = "sys"


def load_sys(hostname, **kwargs):
    PWD = os.getenv("SYS_SUPERUSER_PWD")
    if PWD is None:
        raise ValueError("SYS_SUPERUSER_PWD environment variable is not set")
    url = urljoin(hostname, "api/auth/user/register")
    res = requests.post(
        url, json={"user_name": SYS_USER_NAME, "password": PWD}, **kwargs
    )
    if not res.ok:
        raise Exception(res.text)
    return res.json()


def assign_superuser_role(hostname, **kwargs):
    url = urljoin(hostname, "api/auth/user/roles:add")
    res = requests.post(
        url, json={"user_name": SYS_USER_NAME, "roles": ["superuser"]}, **kwargs
    )
    if not res.ok:
        raise Exception(res.text)
    return res.json()


def load(hostname: str, *args, **kwargs) -> None:
    roles = load_roles(hostname, **kwargs)
    permissions = load_permissions(hostname, **kwargs)
    assign_perms_to_superuser(
        hostname,
        roles[0]["auth_role_id"],
        [p["auth_permission_code"] for p in permissions],
        **kwargs,
    )
    load_sys(hostname, **kwargs)
    assign_superuser_role(hostname, **kwargs)
