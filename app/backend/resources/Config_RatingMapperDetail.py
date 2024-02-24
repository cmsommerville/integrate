from flask import request
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRatingMapperDetail
from ..schemas import Schema_ConfigRatingMapperDetail


class CRUD_ConfigRatingMapperDetail(BaseCRUDResource):
    model = Model_ConfigRatingMapperDetail
    schema = Schema_ConfigRatingMapperDetail()


class CRUD_ConfigRatingMapperDetail_List(BaseCRUDResourceList):
    model = Model_ConfigRatingMapperDetail
    schema = Schema_ConfigRatingMapperDetail(many=True)
