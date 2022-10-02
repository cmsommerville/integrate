from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRateTable
from ..schemas import Schema_ConfigRateTable

class CRUD_ConfigRateTable(BaseCRUDResource): 
    model = Model_ConfigRateTable
    schema = Schema_ConfigRateTable()

class CRUD_ConfigRateTable_List(BaseCRUDResourceList): 
    model = Model_ConfigRateTable
    schema = Schema_ConfigRateTable(many=True)