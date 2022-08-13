from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigRateTable

class Schema_ConfigRateTable(BaseSchema):
    class Meta:
        model = Model_ConfigRateTable
        load_instance = True
        include_relationships=True
        include_fk=True