from flask_restx import Namespace
from ..resources import *

ns_getters = Namespace("getters", "Namespace containing custom GET endpoints")
ns_getters.add_resource(
    Data_ConfigBenefit, "/config/product/<int:product_id>/benefit/<int:id>"
)
ns_getters.add_resource(
    Data_ConfigBenefit_List, "/config/product/<int:product_id>/benefits"
)

ns_getters.add_resource(Progress_ConfigProduct, "/config/product/<int:id>/progress")
