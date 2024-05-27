from flask_restx import Namespace
from app.backend import resources as res

ns_dd = Namespace("dropdowns", "Namespace containing standard dropdown endpoints")

ns_dd.add_resource(
    res.Getter_ConfigProductVariationState_SelectionPlan, "/product_variation_states"
)
ns_dd.add_resource(
    res.Getter_ConfigBenefits_SelectionPlan, "/plan/<int:selection_plan_id>/benefits"
)
