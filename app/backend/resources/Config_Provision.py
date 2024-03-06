from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import (
    Model_ConfigProvision,
)
from ..schemas import (
    Schema_ConfigProvision,
)
from ..validators.Config_Provision import (
    Validator_ConfigProvision,
    Validator_ConfigProvisionList,
)


class CRUD_ConfigProvision(BaseCRUDResource):
    model = Model_ConfigProvision
    schema = Schema_ConfigProvision()
    validator = Validator_ConfigProvision


class CRUD_ConfigProvision_List(BaseCRUDResourceList):
    model = Model_ConfigProvision
    schema = Schema_ConfigProvision(many=True)
    validator = Validator_ConfigProvisionList
