from flask import request, current_app
from flask_restx import Resource
from app.extensions import db
from app.shared import BaseTemporalTable


class Resource_AdminDropTables(Resource):

    @classmethod
    def post(cls):
        try:
            # drop system versioning if supported
            if current_app.config.get("SUPPORT_TEMPORAL_TABLES", False):
                tables = [BaseTemporalTable(tbl) for nm, tbl in db.metadata.tables.items()]
                for tbl in tables:
                    tbl.drop_system_versioning(db)

        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

        try: 
            db.drop_all()
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
        else:
            return {"message": "Success"}, 200

