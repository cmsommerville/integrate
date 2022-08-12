from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProvision_Product, Model_ConfigProvision_RateTable
from ..schemas import Schema_ConfigProvision_Product, Schema_ConfigProvision_RateTable

class CRUD_ConfigProvision_Product(BaseCRUDResource): 
    model = Model_ConfigProvision_Product
    schema = Schema_ConfigProvision_Product

class CRUD_ConfigProvision_Product_List(BaseCRUDResourceList): 
    model = Model_ConfigProvision_Product
    schema = Schema_ConfigProvision_Product

class CRUD_ConfigProvision_RateTable(BaseCRUDResource): 
    model = Model_ConfigProvision_RateTable
    schema = Schema_ConfigProvision_RateTable

class CRUD_ConfigProvision_RateTable_List(BaseCRUDResourceList): 
    model = Model_ConfigProvision_RateTable
    schema = Schema_ConfigProvision_RateTable