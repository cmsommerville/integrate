from flask_restx import Namespace
from app.backend import resources as res

ns_diagnostics = Namespace("diagnostics", "Namespace containing diagnostic endpoints")

ns_diagnostics.add_resource(
    res.Resource_Diagnostics_ConfigProductVariation,
    "/variation/<int:id>/states:benefits",
)
ns_diagnostics.add_resource(
    res.Resource_Diagnostics_ConfigProductVariationState,
    "/variation-state/<int:id>/states:benefits",
)
