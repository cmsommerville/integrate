from app.shared import BaseSchema

from ..models import Model_AuthPermission


class Schema_AuthPermission(BaseSchema):
    class Meta:
        model = Model_AuthPermission
        load_instance = True
