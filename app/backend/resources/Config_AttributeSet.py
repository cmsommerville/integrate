from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import (
    Model_ConfigAttributeSet,
)
from ..schemas import (
    Schema_ConfigAttributeSet,
)


class CRUD_ConfigAttributeSet(BaseCRUDResource):
    model = Model_ConfigAttributeSet
    schema = Schema_ConfigAttributeSet()


class CRUD_ConfigAttributeSet_List(BaseCRUDResourceList):
    model = Model_ConfigAttributeSet
    schema = Schema_ConfigAttributeSet(many=True)
