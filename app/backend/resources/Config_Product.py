from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigProduct
from ..schemas import Schema_ConfigProduct
from ..auth import API_ROLE_SUPERUSER

class CRUD_ConfigProduct(BaseCRUDResource): 
    model = Model_ConfigProduct
    schema = Schema_ConfigProduct()

class CRUD_ConfigProduct_List(BaseCRUDResourceList): 
    model = Model_ConfigProduct
    schema = Schema_ConfigProduct(many=True)