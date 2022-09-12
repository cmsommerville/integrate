from app.extensions import ma
from app.shared import BaseSchema, PrimitiveField

from ..models import Model_SelectionProvision
from .Config_Provision import Schema_ConfigProvision


class Schema_SelectionProvision(BaseSchema):
    class Meta:
        model = Model_SelectionProvision
        load_instance = True
        include_relationships=True
        include_fk=True

    config_provision = ma.Nested(Schema_ConfigProvision)
    is_product_factor = ma.Boolean(dump_only=True)