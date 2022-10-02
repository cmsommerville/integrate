from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductVariationState
from ..schemas import Schema_ConfigProductVariationState

class CRUD_ConfigProductVariationState(BaseCRUDResource): 
    model = Model_ConfigProductVariationState
    schema = Schema_ConfigProductVariationState()

class CRUD_ConfigProductVariationState_List(BaseCRUDResourceList): 
    model = Model_ConfigProductVariationState
    schema = Schema_ConfigProductVariationState(many=True)