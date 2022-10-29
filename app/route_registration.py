from app.backend.routes import ns_crud, ns_dd, ns_getters
from app.admin.routes import ns_admin
from app.auth.routes import ns_auth

NAMESPACES = [
    ns_dd, 
    ns_getters, 
    ns_crud, 
    ns_admin,
    ns_auth, 
]