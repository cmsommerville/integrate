from app.extensions import ma
from app.shared import BaseSchema, PrimitiveField

from ..models import Model_SelectionRateTable
from .Selection_AgeBand import Schema_SelectionAgeBand
from .Config_AttributeDetail import Schema_ConfigAttributeDetail
from .Config_RateGroup import Schema_ConfigRateGroup


class Schema_SelectionRateTable(BaseSchema):
    class Meta:
        model = Model_SelectionRateTable
        load_instance = True
        include_relationships=True
        include_fk=True

    age_band = ma.Nested(Schema_SelectionAgeBand)
    config_rate_group = ma.Nested(Schema_ConfigRateGroup)
    gender = ma.Nested(Schema_ConfigAttributeDetail)
    smoker_status = ma.Nested(Schema_ConfigAttributeDetail)
    relationship = ma.Nested(Schema_ConfigAttributeDetail)