from flask import request
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

    @classmethod
    def delete(cls):
        plan_id = request.args.get('plan_id')
        if plan_id is None:
            return {"status": "error", "msg": "Please provide a query parameter `plan_id`"}, 400
        Model_SelectionRateGroupFaceAmounts.delete_by_plan(plan_id)
        return {"status": "success", "msg": "Deleted face amounts for provided plan id"}, 200