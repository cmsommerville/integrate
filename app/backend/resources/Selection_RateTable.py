import pandas as pd
from flask_restx import Resource
from ..models import Model_SelectionRateTable
from ..schemas import Schema_SelectionRateTable

class Resource_SelectionRateTable(Resource): 

    @classmethod
    def get(cls, plan_id: int):
        _schema_list = Schema_SelectionRateTable(many=True)
        rate_tables = Model_SelectionRateTable.find_by_plan(plan_id)
        return _schema_list.dump(rate_tables), 201
