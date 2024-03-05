from flask_restx import Namespace

from . import resources as res

ns_admin = Namespace("admin", description="Reference data REST API")

ns_admin.add_resource(res.Resource_AdminAssignUserRole, *["/user/roles:add"])
ns_admin.add_resource(res.Resource_AdminRemoveUserRole, *["/user/roles:remove"])
ns_admin.add_resource(res.Resource_AdminCreateTables, *["/tables:create"])
ns_admin.add_resource(res.Resource_AdminDeleteTables, *["/tables:delete"])
ns_admin.add_resource(res.Resource_AdminDropTables, *["/tables:drop"])
ns_admin.add_resource(res.Resource_AdminInitRefData, *["/data/load:refdata"])
ns_admin.add_resource(res.Resource_AdminLoadData, *["/data/load:generic"])
ns_admin.add_resource(res.Resource_AdminInitConfig, *["/data/load:config"])
ns_admin.add_resource(res.Resource_RandomSelectionPlan, *["/data/create:random-plan"])
ns_admin.add_resource(res.Resource_AdminHealthCheck, *["/health"])
ns_admin.add_resource(res.Resource_ConfigProductLoader, *["/data/load:product"])
