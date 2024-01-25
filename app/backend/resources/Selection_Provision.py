from itertools import product
from flask import request
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_SelectionProvision, Model_SelectionRateTableFactor
from ..schemas import Schema_SelectionProvision
from ..classes import RulesetApplicator


class CRUD_SelectionProvision(BaseCRUDResource): 
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision()



class CRUD_SelectionProvision_List(BaseCRUDResourceList): 
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision(many=True)
