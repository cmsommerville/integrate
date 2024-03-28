from flask import request
from flask_restx import Resource
from app.extensions import db
from app.shared import BaseReflectedModel


class Resource_AdminDeleteTables(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            if data is None:
                data = {}
            schema = data.get("schema", "dbo")

            model_classes = [x.class_ for x in db.Model.registry.mappers]
            managed_tables = set(
                [
                    x.__table__
                    for x in model_classes
                    if not issubclass(x, BaseReflectedModel)
                ]
            )

            tables = [tbl for tbl in db.metadata.sorted_tables if tbl in managed_tables]
            for table in reversed(tables):
                table_schema = getattr(table, "schema")
                if table_schema is None and schema == "dbo":
                    db.session.execute(table.delete())
                elif table_schema == schema:
                    db.session.execute(table.delete())

            db.session.commit()
            return {"status": "success", "msg": "All table data has been deleted!"}
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "msg": "Could not delete from all tables",
                "traceback": str(e),
            }
