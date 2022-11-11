from flask_restx import Namespace

from .resources import *

ns_auth = Namespace('auth', description='Authentication REST API')

ns_auth.add_resource(Resource_AuthRoles, *['/auth/roles'])
ns_auth.add_resource(Resource_AuthLogin, *['/auth/user/login'])
ns_auth.add_resource(Resource_AuthSetPassword, *['/auth/user/password/set'])
ns_auth.add_resource(Resource_AuthRegister, *['/auth/user/register'])
ns_auth.add_resource(Resource_AuthManageUserRole, *['/auth/user/roles'])

