from flask_restx import Namespace

from .resources import *

ns_auth = Namespace('auth', description='Authentication REST API')

ns_auth.add_resource(Resource_AuthLogin, *['/auth/login'])
ns_auth.add_resource(Resource_AuthSetPassword, *['/auth/password/set'])
ns_auth.add_resource(Resource_AuthRegister, *['/auth/register'])

