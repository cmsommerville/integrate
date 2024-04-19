from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRatingMapperCollection
from ..schemas import Schema_ConfigRatingMapperCollection


class CRUD_ConfigRatingMapperCollection(BaseCRUDResource):
    model = Model_ConfigRatingMapperCollection
    schema = Schema_ConfigRatingMapperCollection()


class CRUD_ConfigRatingMapperCollection_List(BaseCRUDResourceList):
    model = Model_ConfigRatingMapperCollection
    schema = Schema_ConfigRatingMapperCollection(many=True)
