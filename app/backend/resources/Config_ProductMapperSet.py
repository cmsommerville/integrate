from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProductMapperSet_Gender,  Model_ConfigProductMapperSet_SmokerStatus
from ..schemas import Schema_ConfigProductMapperSet_Gender, Schema_ConfigProductMapperSet_SmokerStatus

class CRUD_ConfigProductMapperSet_Gender(BaseCRUDResource): 
    model = Model_ConfigProductMapperSet_Gender
    schema = Schema_ConfigProductMapperSet_Gender()

class CRUD_ConfigProductMapperSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigProductMapperSet_Gender
    schema = Schema_ConfigProductMapperSet_Gender(many=True)

class CRUD_ConfigProductMapperSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigProductMapperSet_SmokerStatus
    schema = Schema_ConfigProductMapperSet_SmokerStatus()

class CRUD_ConfigProductMapperSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigProductMapperSet_SmokerStatus
    schema = Schema_ConfigProductMapperSet_SmokerStatus(many=True)