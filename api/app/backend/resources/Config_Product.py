from typing import List
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProduct
from ..schemas import Schema_ConfigProduct


class CRUD_ConfigProduct(BaseCRUDResource):
    model = Model_ConfigProduct
    schema = Schema_ConfigProduct()


class CRUD_ConfigProduct_List(BaseCRUDResourceList):
    model = Model_ConfigProduct
    schema = Schema_ConfigProduct(many=True)


class Progress_ConfigProduct(Resource):
    @classmethod
    def _progress_tracker(cls, product: Model_ConfigProduct, requirements: List[str]):
        completed = sum(
            [1 for r in requirements if getattr(product, r, None) is not None]
        )
        return completed / len(requirements)

    @classmethod
    def get(cls, id):
        product = Model_ConfigProduct.find_one(id)
        if product is None:
            return {"status": "error", "msg": "Cannot find product ID"}

        prog_attrs = cls._progress_tracker(
            product,
            [
                "gender_attr_set_id",
                "smoker_status_attr_set_id",
                "relationship_attr_set_id",
            ],
        )

        prog_dists = cls._progress_tracker(
            product,
            [
                "gender_distribution_set_id",
                "smoker_status_distribution_set_id",
                "age_distribution_set_id",
            ],
        )

        prog_strategies = cls._progress_tracker(
            product,
            [
                "gender_rating_strategy_id",
                "smoker_status_rating_strategy_id",
                "age_rating_strategy_id",
            ],
        )

        return {
            "config_product_id": product.config_product_id,
            "progress": {
                "attrs": prog_attrs,
                "dists": prog_dists,
                "strategies": prog_strategies,
            },
        }, 200
