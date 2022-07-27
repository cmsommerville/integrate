from flask_restx import Namespace
from .resources import *

ns_admin = Namespace('admin', description='Reference data REST API')

ns_admin.add_resource(Resource_AdminCreateTables, *['/admin/create-tables'])
ns_admin.add_resource(Resource_AdminDropTables, *['/admin/drop-tables'])
ns_admin.add_resource(Resource_AdminHealthCheck, *['/admin/health'])

