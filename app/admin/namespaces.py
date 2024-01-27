from flask_restx import Namespace

from . import resources as res

ns_admin = Namespace("admin", description="Reference data REST API")

ns_admin.add_resource(res.Resource_AdminAssignUserRole, *["/user/roles/add"])
ns_admin.add_resource(res.Resource_AdminRemoveUserRole, *["/user/roles/remove"])
ns_admin.add_resource(res.Resource_AdminCreateTables, *["/tables/_create"])
ns_admin.add_resource(res.Resource_AdminDeleteTables, *["/tables/_delete"])
ns_admin.add_resource(res.Resource_AdminDropTables, *["/tables/_drop"])
ns_admin.add_resource(res.Resource_AdminInitRefData, *["/tables/_load/refdata"])
ns_admin.add_resource(res.Resource_AdminInitConfig, *["/tables/_load/config"])
ns_admin.add_resource(res.Resource_AdminInitRateTable, *["/tables/_load/rate-table"])
ns_admin.add_resource(res.Resource_AdminHealthCheck, *["/health"])
