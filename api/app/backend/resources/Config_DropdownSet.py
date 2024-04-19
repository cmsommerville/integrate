from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigDropdownSet
from ..schemas import Schema_ConfigDropdownSet


class CRUD_ConfigDropdownSet(BaseCRUDResource):
    model = Model_ConfigDropdownSet
    schema = Schema_ConfigDropdownSet(exclude=("_dropdown_details",))


class CRUD_ConfigDropdownSet_List(BaseCRUDResourceList):
    model = Model_ConfigDropdownSet
    schema = Schema_ConfigDropdownSet(many=True, exclude=("_dropdown_details",))
