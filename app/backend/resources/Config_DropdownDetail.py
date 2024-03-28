from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigDropdownDetail
from ..schemas import Schema_ConfigDropdownDetail


class CRUD_ConfigDropdownDetail(BaseCRUDResource):
    model = Model_ConfigDropdownDetail
    schema = Schema_ConfigDropdownDetail()


class CRUD_ConfigDropdownDetail_List(BaseCRUDResourceList):
    model = Model_ConfigDropdownDetail
    schema = Schema_ConfigDropdownDetail(many=True)
