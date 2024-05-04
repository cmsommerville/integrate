from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigCoverage

class Schema_ConfigCoverage(BaseSchema):
    class Meta:
        model = Model_ConfigCoverage
        load_instance = True
        include_relationships=True
        include_fk=True
