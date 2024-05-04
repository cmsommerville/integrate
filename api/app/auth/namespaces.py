from flask_restx import Namespace

from . import resources as res

ns_auth = Namespace(
    "Authentication Routes",
    description="Login, registration, and access management routes",
)

ns_auth.add_resource(res.Resource_AuthPermissions, *["/permissions"])
ns_auth.add_resource(res.Resource_AuthRoles, *["/roles"])
ns_auth.add_resource(
    res.Resource_AuthManageRolePermissions, *["/role/<int:id>/permissions"]
)
ns_auth.add_resource(res.Resource_AuthLogin, *["/user/login"])
ns_auth.add_resource(res.Resource_AuthSetPassword, *["/user:password"])
ns_auth.add_resource(res.Resource_AuthRegister, *["/user/register"])
ns_auth.add_resource(res.Resource_AdminAssignUserRole, *["/admin/user/roles:add"])
ns_auth.add_resource(res.Resource_AdminRemoveUserRole, *["/admin/user/roles:remove"])
ns_auth.add_resource(res.Resource_AdminCreateNewUser, *["/admin/user:new"])
ns_auth.add_resource(
    res.Resource_AdminResetUserPassword, *["/admin/user:reset-password"]
)
