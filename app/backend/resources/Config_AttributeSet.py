from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList, BaseObservable
from ..models import Model_ConfigAttributeSet_Gender, Model_ConfigAttributeSet_SmokerStatus, Model_ConfigAttributeSet_Relationship
from ..schemas import Schema_ConfigAttributeSet_Gender, Schema_ConfigAttributeSet_SmokerStatus,  Schema_ConfigAttributeSet_Relationship

class CRUD_ConfigAttributeSet_Gender(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender

class CRUD_ConfigAttributeSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender

class CRUD_ConfigAttributeSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus

class CRUD_ConfigAttributeSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus

class CRUD_ConfigAttributeSet_Relationship(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Gender

class CRUD_ConfigAttributeSet_Relationship_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Relationship