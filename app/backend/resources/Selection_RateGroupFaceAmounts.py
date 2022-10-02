from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionRateGroupFaceAmounts
from ..schemas import Schema_SelectionRateGroupFaceAmounts

class CRUD_SelectionRateGroupFaceAmounts(BaseCRUDResource): 
    model = Model_SelectionRateGroupFaceAmounts
    schema = Schema_SelectionRateGroupFaceAmounts()

class CRUD_SelectionRateGroupFaceAmounts_List(BaseCRUDResourceList): 
    model = Model_SelectionRateGroupFaceAmounts
    schema = Schema_SelectionRateGroupFaceAmounts(many=True)

