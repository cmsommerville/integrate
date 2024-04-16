import time
from sqlalchemy.sql import text
from sqlalchemy.dialects.mssql import DATETIME2
from app.extensions import db
from flask_restx import Resource


class TestModel(db.Model):
    __tablename__ = "testtbl"

    id = db.Column(db.Integer, primary_key=True)
    asofdts = db.Column(DATETIME2, nullable=False)

    @classmethod
    def add_system_versioning(
        cls,
        row_eff_dts="row_eff_dts",
        row_exp_dts="row_exp_dts",
        *args,
        **kwargs,
    ):
        """
        Enable system versioning on this table. First, add the row eff/exp dates. Then, add a history table.
        """
        HISTORY_TABLE_NAME = f"dbo.{cls.__tablename__}_history"

        sql = f"""
        ALTER TABLE {cls.__tablename__}
        ADD 
            {row_eff_dts} DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL DEFAULT GETUTCDATE(),
            {row_exp_dts} DATETIME2 GENERATED ALWAYS AS ROW END NOT NULL DEFAULT CONVERT(DATETIME2, '9999-12-31 00:00:00.0000000'),
        PERIOD FOR SYSTEM_TIME ({row_eff_dts}, {row_exp_dts})
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()

        sql = f"""
        ALTER TABLE {cls.__tablename__}
        SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE={HISTORY_TABLE_NAME}))
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()


class TestResource(Resource):
    def get(self, *args, **kwargs):
        # setup the table
        db.create_all()
        TestModel.add_system_versioning()
        return {"hello": "world"}

    def post(self, *args, **kwargs):
        # get the current UTC datetime from the database (which is what the row_eff_dts should use too!)
        with db.session.begin():
            asofdts, transaction_id = db.session.execute(
                text(
                    "SELECT CAST(GETUTCDATE() AS DATETIME2) AS asofdts, CURRENT_TRANSACTION_ID() AS transaction_id"
                )
            ).first()
            print(transaction_id)

        # with db.session.begin():
        _, transaction_id = db.session.execute(
            text(
                "SELECT CAST(GETUTCDATE() AS DATETIME2) AS asofdts, CURRENT_TRANSACTION_ID() AS transaction_id"
            )
        ).first()
        print(transaction_id)
        # create a new row
        obj = TestModel(asofdts=asofdts)
        db.session.add(obj)
        db.session.commit()

        return {"hello": "world"}
