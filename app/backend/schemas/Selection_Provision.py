from marshmallow import Schema, fields, EXCLUDE
from app.shared import BaseSchema

from ..models import Model_SelectionProvision


class Schema_SelectionProvision(BaseSchema):
    class Meta:
        model = Model_SelectionProvision
        load_instance = True
        include_relationships = True
        include_fk = True


class Schema_SelectionProvision_UpdatePayloadValidator(Schema):
    selection_value = fields.Str()

    class Meta:
        unknown = EXCLUDE


class Schema_SelectionProvision_CreatePayloadValidator(Schema):
    selection_plan_id = fields.Int()
    config_provision_id = fields.Int()
    selection_value = fields.Str()

    class Meta:
        unknown = EXCLUDE
