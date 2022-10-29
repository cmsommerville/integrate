from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_AuthUser
from .AuthRole import Schema_AuthRole

class Schema_AuthUser(BaseSchema):
    class Meta:
        model = Model_AuthUser
        load_instance = True
        include_fk = True
        include_relationships = True

    user_id = ma.Integer()
    user_name = ma.String()
    hashed_password = ma.Raw(load_only=True)

    roles = ma.Nested(Schema_AuthRole, many=True)