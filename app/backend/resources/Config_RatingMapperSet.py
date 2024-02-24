from app.shared import BaseCRUDResource, BaseCRUDResourceList
from app.auth import authorization_required
from ..models import Model_ConfigRatingMapperSet
from ..schemas import Schema_ConfigRatingMapperSet


class CRUD_ConfigRatingMapperSet(BaseCRUDResource):
    model = Model_ConfigRatingMapperSet
    schema = Schema_ConfigRatingMapperSet()


class CRUD_ConfigRatingMapperSet_List(BaseCRUDResourceList):
    model = Model_ConfigRatingMapperSet
    schema = Schema_ConfigRatingMapperSet(many=True)

    @classmethod
    def get(cls, collection_id: int, *args, **kwargs):
        try:
            objs = cls.model.find_all_by_attr(
                {"config_rating_mapper_collection_id": collection_id}
            )
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

        try:
            if objs:
                return cls.schema.dump(objs), 200
            raise Exception("No data found")
        except Exception:
            return [], 200
