from flask import request, current_app
from flask_restx import Resource
from app.extensions import db
from app.shared import BaseModel, BaseTemporalTable, BaseRowLevelSecurityTable


class Resource_AdminDeleteTables(Resource):

    @classmethod
    def post(cls):
        try: 
            data = request.get_json()
            if data is None:
                data = {}
            schema = data.get('schema', 'dbo')

            tables = db.metadata.sorted_tables
            for table in reversed(tables):
                table_schema = getattr(table, 'schema')
                if table_schema is None and schema == 'dbo':
                    db.session.execute(table.delete())
                elif table_schema == schema: 
                    db.session.execute(table.delete())

            db.session.commit()
            return {"status": "success", "message": "All table data has been deleted!"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": "Could not delete from all tables", "traceback": str(e)}