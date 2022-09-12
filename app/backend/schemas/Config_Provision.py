from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvision, Model_ConfigProvision_Product, Model_ConfigProvision_RateTable

class Schema_ConfigProvision(BaseSchema):
    class Meta:
        model = Model_ConfigProvision
        load_instance = True
        include_relationships=True
        include_fk=True

class Schema_ConfigProvision_Product(BaseSchema):
    class Meta:
        model = Model_ConfigProvision_Product
        load_instance = True
        include_relationships=True
        include_fk=True

    config_provision_type_code = ma.Constant('product')

class Schema_ConfigProvision_RateTable(BaseSchema):
    class Meta:
        model = Model_ConfigProvision_RateTable
        load_instance = True
        include_relationships=True
        include_fk=True

    config_provision_type_code = ma.Constant('rate_table')

