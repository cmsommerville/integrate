from flask_restx import Resource


class Resource_AdminHealthCheck(Resource):

    @classmethod
    def get(cls): 
        return {"status": "Application running"}