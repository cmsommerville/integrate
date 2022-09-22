from flask_restx import Resource
from app.backend.observables import Observable_SelectionProvision


class REST_Observable_SelectionProvision(Resource): 

    @classmethod
    def get(cls): 
        return [str(x) for x in Observable_SelectionProvision.observers], 200