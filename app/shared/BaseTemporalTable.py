from sqlalchemy import Table
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy


class BaseTemporalTable:
    def __init__(self, table: Table):
        self.table = table
        self.schema = table.schema if table.schema else "dbo"
        self._q_table_name = f"{self.schema}.{table.name}"
        self._q_history_table_name = f"{self._q_table_name}_history"

    def add_system_versioning(
        self,
        db: SQLAlchemy,
        row_eff_dts="row_eff_dts",
        row_exp_dts="row_exp_dts",
        *args,
        **kwargs,
    ):
        """
        Enable system versioning on this table. First, add the row eff/exp dates. Then, add a history table.
        """
        sql = f"""
        ALTER TABLE {self._q_table_name}
        ADD 
            {row_eff_dts} DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL DEFAULT GETUTCDATE(),
            {row_exp_dts} DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN  NOT NULL DEFAULT CONVERT(DATETIME2, '9999-12-31 00:00:00.0000000'),
        PERIOD FOR SYSTEM_TIME ({row_eff_dts}, {row_exp_dts})
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()

        sql = f"""
        ALTER TABLE {self._q_table_name}
        SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE={self._q_history_table_name}))
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()

    def drop_system_versioning(self, db: SQLAlchemy, *args, **kwargs):
        """
        Turn off system versioning on this table. Then drop the history table.
        """
        sql = f"""
        ALTER TABLE {self._q_table_name} SET ( SYSTEM_VERSIONING = OFF )
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()

        sql = f"""
        DROP TABLE {self._q_history_table_name}
        """
        try:
            db.session.execute(text(sql))
            db.session.commit()
        except Exception:
            db.session.rollback()
