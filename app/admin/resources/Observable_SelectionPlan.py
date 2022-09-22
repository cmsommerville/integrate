from flask_restx import Resource
from app.backend.observables import Observable_SelectionPlan


class REST_Observable_SelectionPlan(Resource): 

    @classmethod
    def get(cls): 
        return [str(x) for x in Observable_SelectionPlan.observers], 200