from flask_restx import Resource
from ..models import Model_SelectionBenefitRateTable, Model_SelectionRateTable
from ..schemas import Schema_SelectionRateTable

class CRUD_SelectionBenefitRateTable(Resource): 

    @classmethod
    def post(cls, plan_id: int):
        _schema_list = Schema_SelectionRateTable(many=True)
        Model_SelectionBenefitRateTable.create_rate_table(plan_id)
        rate_tables = Model_SelectionRateTable.find_by_plan(plan_id)
        return _schema_list.dump(rate_tables), 201
