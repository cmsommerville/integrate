from flask_restx import Resource
from ..models import Model_DefaultProductRatingMapperSet
from ..schemas import (
    Schema_DefaultProductRatingMapperSet_For_Selection,
    Schema_SelectionRatingMapperSet,
)


class TestResource(Resource):
    schema = Schema_DefaultProductRatingMapperSet_For_Selection(many=True)
    selection_schema = Schema_SelectionRatingMapperSet(many=True)

    @classmethod
    def get(cls, parent_id: int, *args, **kwargs):
        objs = Model_DefaultProductRatingMapperSet.find_by_parent(parent_id)
        data = cls.schema.dump(objs)
        selection_objs = cls.selection_schema.load(
            [{**row, "selection_plan_id": parent_id} for row in data]
        )
        return cls.selection_schema.dump(selection_objs), 200
