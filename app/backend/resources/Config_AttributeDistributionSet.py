from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAttributeDistributionSet_Gender, Model_ConfigAttributeDistributionSet_SmokerStatus
from ..schemas import Schema_ConfigAttributeDistributionSet_Gender, Schema_ConfigAttributeDistributionSet_SmokerStatus

class CRUD_ConfigAttributeDistributionSet_Gender(BaseCRUDResource): 
    model = Model_ConfigAttributeDistributionSet_Gender
    schema = Schema_ConfigAttributeDistributionSet_Gender

class CRUD_ConfigAttributeDistributionSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDistributionSet_Gender
    schema = Schema_ConfigAttributeDistributionSet_Gender

class CRUD_ConfigAttributeDistributionSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigAttributeDistributionSet_SmokerStatus
    schema = Schema_ConfigAttributeDistributionSet_SmokerStatus

class CRUD_ConfigAttributeDistributionSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeDistributionSet_SmokerStatus
    schema = Schema_ConfigAttributeDistributionSet_SmokerStatus