from flask import request
from flask_restx import Resource
from app.extensions import db


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
            return {"status": "success", "msg": "All table data has been deleted!"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": "Could not delete from all tables", "traceback": str(e)}