from flask_restx import Namespace
from app.backend import resources as res
from .util import add_routes

ns_selection_rpc = Namespace(
    "Selection RPC routes",
    "Namespace containing standard RPC endpoints for selection events",
)

SELECTION_RPC_ROUTES = {
    "/plan/<int:parent_id>/<string:event>": res.Resource_Selection_RPC_Dispatcher,
    "/plan/<string:event>": res.Resource_Selection_RPC_Dispatcher,
}

add_routes(ns_selection_rpc, SELECTION_RPC_ROUTES)
