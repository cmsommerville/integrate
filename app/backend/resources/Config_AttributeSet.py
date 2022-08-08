from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList, BaseObservable
from ..models import Model_ConfigAttributeSet_Gender, Model_ConfigAttributeSet_SmokerStatus, Model_ConfigAttributeSet_Relationship
from ..schemas import Schema_ConfigAttributeSet_Gender, Schema_ConfigAttributeSet_SmokerStatus,  Schema_ConfigAttributeSet_Relationship
from ..observables import Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_Gender(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender
    observable = Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_Gender_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Gender
    schema = Schema_ConfigAttributeSet_Gender
    observable = Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_SmokerStatus(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus
    observable = Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_SmokerStatus_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_SmokerStatus
    schema = Schema_ConfigAttributeSet_SmokerStatus
    observable = Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_Relationship(BaseCRUDResource): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Gender
    observable = Observable_ConfigAttributeSet

class CRUD_ConfigAttributeSet_Relationship_List(BaseCRUDResourceList): 
    model = Model_ConfigAttributeSet_Relationship
    schema = Schema_ConfigAttributeSet_Relationship
    observable = Observable_ConfigAttributeSet