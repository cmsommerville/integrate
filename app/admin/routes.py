from flask_restx import Namespace

from .resources import *

ns_admin = Namespace('admin', description='Reference data REST API')

ns_admin.add_resource(Resource_AdminAssignUserRole, *['/admin/user/roles/add'])
ns_admin.add_resource(Resource_AdminRemoveUserRole, *['/admin/user/roles/remove'])
ns_admin.add_resource(Resource_AdminCreateTables, *['/admin/tables/_create'])
ns_admin.add_resource(Resource_AdminDropTables, *['/admin/tables/_drop'])
ns_admin.add_resource(Resource_AdminInitRefData, *['/admin/tables/_load/refdata'])
ns_admin.add_resource(Resource_AdminInitConfig, *['/admin/tables/_load/config'])
ns_admin.add_resource(Resource_AdminInitRateTable, *['/admin/tables/_load/rate-table'])
ns_admin.add_resource(Resource_AdminHealthCheck, *['/admin/health'])
ns_admin.add_resource(Resource_AdminSelectionData, *['/admin/tables/_load/selections'])

ns_admin.add_resource(REST_Observable_SelectionPlan, '/admin/observables/selection/plan')
ns_admin.add_resource(REST_Observable_SelectionProvision, '/admin/observables/selection/provision')


