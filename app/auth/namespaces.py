from flask_restx import Namespace

from .resources import *

ns_auth = Namespace('auth', description='Authentication REST API')

ns_auth.add_resource(Resource_AuthRoles, *['/roles'])
ns_auth.add_resource(Resource_AuthLogin, *['/user/login'])
ns_auth.add_resource(Resource_AuthSetPassword, *['/user/password/set'])
ns_auth.add_resource(Resource_AuthRegister, *['/user/register'])
ns_auth.add_resource(Resource_AuthManageUserRole, *['/user/roles'])

