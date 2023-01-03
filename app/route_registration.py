from app.backend.routes import NAMESPACES as NS_BACKEND
from app.admin.routes import NAMESPACES as NS_ADMIN
from app.auth.routes import NAMESPACES as NS_AUTH

NAMESPACES = [
    *NS_BACKEND, 
    *NS_ADMIN, 
    *NS_AUTH
]