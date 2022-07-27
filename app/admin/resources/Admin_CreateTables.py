from flask import request, current_app
from flask_restx import Resource
from app.extensions import db
from app.shared import BaseTemporalTable


class Resource_AdminCreateTables(Resource):

    @classmethod
    def post(cls):
        try:
            db.create_all()

            # add system versioning if supported
            if current_app.config.get("SUPPORT_TEMPORAL_TABLES"):
                tables = [BaseTemporalTable(tbl) for nm, tbl in db.metadata.tables.items()]
                for tbl in tables:
                    tbl.add_system_versioning(db)

        except Exception as e:
            return str(e), 400
        else:
            return {"message": "Success"}, 200

