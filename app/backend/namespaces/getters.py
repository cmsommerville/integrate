from flask_restx import Namespace
from ..resources import *

ns_getters = Namespace("getters", "Namespace containing custom GET endpoints")
ns_getters.add_resource(Data_ConfigBenefit, '/config/product/<int:product_id>/benefit/<int:id>')
ns_getters.add_resource(Data_ConfigBenefit_List, '/config/product/<int:product_id>/benefits')

ns_getters.add_resource(Resource_SelectionPlan_ConfigProduct, '/selection/plan/<int:id>/product')
ns_getters.add_resource(Resource_SelectionPlan_GenderProductMapper, '/selection/plan/<int:id>/gender-mapper-list')
ns_getters.add_resource(Resource_SelectionPlan_SmokerStatusProductMapper, '/selection/plan/<int:id>/smoker-status-mapper-list')
ns_getters.add_resource(Resource_SelectionRateTable, '/selection/plan/<int:plan_id>/rate-table')

ns_getters.add_resource(Progress_ConfigProduct, '/config/product/<int:id>/progress')
