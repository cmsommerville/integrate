from app.backend.routes import ns_crud, ns_dd, ns_getters
from app.admin.routes import ns_admin

NAMESPACES = [
    ns_dd, 
    ns_getters, 
    ns_crud, 
    ns_admin,
]