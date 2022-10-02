from flask_restx import Namespace
from ..resources import *

ns_getters = Namespace("getters", "Namespace containing custom GET endpoints")

ns_getters.add_resource(Resource_SelectionPlan_ConfigProduct, '/data/selection/plan/<int:id>/product')
ns_getters.add_resource(Resource_SelectionPlan_GenderProductMapper, '/data/selection/plan/<int:id>/gender-mapper-list')
ns_getters.add_resource(Resource_SelectionPlan_SmokerStatusProductMapper, '/data/selection/plan/<int:id>/smoker-status-mapper-list')
ns_getters.add_resource(Resource_SelectionRateTable, '/data/selection/plan/<int:plan_id>/rate-table')