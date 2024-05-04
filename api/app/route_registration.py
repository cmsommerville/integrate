from flask import Blueprint
from app.backend.routes import NAMESPACES as NS_BACKEND
from app.backend.routes import RPC_NAMESPACES as NS_RPC
from app.auth.routes import NAMESPACES as NS_AUTH

base_bp = Blueprint("base", __name__)

NAMESPACES = [*NS_BACKEND, *NS_AUTH]
RPC_NAMESPACES = [*NS_RPC]


@base_bp.route("/hello", methods=["GET"])
def hello_world():
    return "<h1>Hello world!</h1>", 200
