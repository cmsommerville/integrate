from app.shared import BaseSchema

from ..models import Model_AuthRolePermission


class Schema_AuthRolePermission(BaseSchema):
    class Meta:
        model = Model_AuthRolePermission
        load_instance = True
        include_fk = True
        include_relationships = True
