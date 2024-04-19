from flask_restx import Resource
from app.auth import authorization_required
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigPlanDesignVariationState
from ..schemas import (
    Schema_ConfigPlanDesignVariationState,
    Schema_ConfigPlanDesignVariationState_CoveragePlanDesignList,
    Schema_ConfigPlanDesignVariationState_ProductPlanDesignList,
)


class CRUD_ConfigPlanDesignVariationState(BaseCRUDResource):
    model = Model_ConfigPlanDesignVariationState
    schema = Schema_ConfigPlanDesignVariationState()


class CRUD_ConfigPlanDesignVariationState_List(BaseCRUDResourceList):
    model = Model_ConfigPlanDesignVariationState
    schema = Schema_ConfigPlanDesignVariationState(many=True)


class Resource_ConfigPlanDesignVariationState_CoveragePlanDesignList(Resource):
    permissions = {"get": ["*"]}

    @classmethod
    @authorization_required
    def get(self, product_variation_state_id: int):
        try:
            objs = Model_ConfigPlanDesignVariationState.find_coverage_plan_designs(
                product_variation_state_id
            )
            schema = Schema_ConfigPlanDesignVariationState_CoveragePlanDesignList(
                many=True
            )
            return schema.dump(objs), 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400


class Resource_ConfigPlanDesignVariationState_ProductPlanDesignList(Resource):
    permissions = {"get": ["*"]}

    @classmethod
    @authorization_required
    def get(self, product_variation_state_id: int):
        try:
            objs = Model_ConfigPlanDesignVariationState.find_product_plan_designs(
                product_variation_state_id
            )
            schema = Schema_ConfigPlanDesignVariationState_ProductPlanDesignList(
                many=True
            )
            return schema.dump(objs), 200
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400
