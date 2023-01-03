from flask_restx import Namespace
from ..resources import *

ns_dd = Namespace("dropdowns", "Namespace containing standard dropdown endpoints")

ns_dd.add_resource(SelectionCensusSet_Dropdown, '/selection/census-set/<int:plan_id>')