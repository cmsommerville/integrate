from flask import current_app
from flask_restx import Resource
from app.extensions import db
from app.shared import BaseTemporalTable, BaseRowLevelSecurityTable, BaseReflectedModel


class Resource_AdminCreateTables(Resource):
    @classmethod
    def post(cls):
        try:
            _handled_tables = []
            model_classes = [x.class_ for x in db.Model.registry.mappers]

            tables = set(
                [
                    x.__table__
                    for x in model_classes
                    if not issubclass(x, BaseReflectedModel)
                ]
            )
            db.metadata.create_all(
                bind=db.engine,
                tables=tables,
            )
            for model in model_classes:
                table_name = model.__tablename__

                if table_name in _handled_tables:
                    continue

                if issubclass(model, BaseReflectedModel):
                    continue

                # add row level security rules
                if issubclass(model, BaseRowLevelSecurityTable):
                    BaseRowLevelSecurityTable.add_rls(model)

                # drop system versioning if supported
                if current_app.config.get("SUPPORT_TEMPORAL_TABLES", False):
                    tbl = BaseTemporalTable(model.__table__)
                    tbl.add_system_versioning(db)

        except Exception as e:
            return str(e), 400
        else:
            return {"msg": "Success"}, 200
