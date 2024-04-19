from app.backend.routes import NAMESPACES as NS_BACKEND
from app.backend.routes import RPC_NAMESPACES as NS_RPC
from app.admin.routes import NAMESPACES as NS_ADMIN
from app.auth.routes import NAMESPACES as NS_AUTH

NAMESPACES = [*NS_BACKEND, *NS_ADMIN, *NS_AUTH]

RPC_NAMESPACES = [*NS_RPC]
