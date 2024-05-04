from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigAgeBandDetail
from ..schemas import Schema_ConfigAgeBandDetail

class CRUD_ConfigAgeBandDetail(BaseCRUDResource): 
    model = Model_ConfigAgeBandDetail
    schema = Schema_ConfigAgeBandDetail()

class CRUD_ConfigAgeBandDetail_List(BaseCRUDResourceList): 
    model = Model_ConfigAgeBandDetail
    schema = Schema_ConfigAgeBandDetail(many=True)