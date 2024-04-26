from .Auth_Login import Resource_AuthLogin
from .Auth_Password import Resource_AuthSetPassword
from .Auth_Permission import Resource_AuthPermissions
from .Auth_Register import Resource_AuthRegister
from .Auth_Roles import Resource_AuthRoles
from .Auth_RolePermission import Resource_AuthManageRolePermissions
from .Auth_UserRoles import Resource_AuthManageUserRole
from .Auth_AdminUserTasks import (
    Resource_AdminCreateNewUser,
    Resource_AdminResetUserPassword,
    Resource_AdminAssignUserRole,
    Resource_AdminRemoveUserRole,
)
