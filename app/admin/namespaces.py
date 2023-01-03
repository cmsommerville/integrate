from flask_restx import Namespace

from .resources import *

ns_admin = Namespace('admin', description='Reference data REST API')

ns_admin.add_resource(Resource_AdminAssignUserRole, *['/user/roles/add'])
ns_admin.add_resource(Resource_AdminRemoveUserRole, *['/user/roles/remove'])
ns_admin.add_resource(Resource_AdminCreateTables, *['/tables/_create'])
ns_admin.add_resource(Resource_AdminDeleteTables, *['/tables/_delete'])
ns_admin.add_resource(Resource_AdminDropTables, *['/tables/_drop'])
ns_admin.add_resource(Resource_AdminInitRefData, *['/tables/_load/refdata'])
ns_admin.add_resource(Resource_AdminInitConfig, *['/tables/_load/config'])
ns_admin.add_resource(Resource_AdminInitRateTable, *['/tables/_load/rate-table'])
ns_admin.add_resource(Resource_AdminHealthCheck, *['/health'])
ns_admin.add_resource(Resource_AdminSelectionData, *['/tables/_load/selections'])

ns_admin.add_resource(REST_Observable_SelectionPlan, '/observables/selection/plan')
ns_admin.add_resource(REST_Observable_SelectionProvision, '/observables/selection/provision')


