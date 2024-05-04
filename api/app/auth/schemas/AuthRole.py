from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_AuthRole

class Schema_AuthRole(BaseSchema):
    class Meta:
        model = Model_AuthRole
        load_instance = True