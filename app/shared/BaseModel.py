from __future__ import annotations
import os
import pandas as pd
from ulid import ULID
from functools import reduce
from flask import current_app
from typing import List
from sqlalchemy import text
from sqlalchemy.sql import text as text_sql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError
from app.auth import get_user


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def version_id(cls):
        return db.Column(
            db.String(26),
            default=lambda: str(ULID()),
            onupdate=lambda: str(ULID()),
        )

    @declared_attr
    def created_dts(cls):
        return db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))

    @declared_attr
    def updated_dts(cls):
        return db.Column(
            db.DateTime,
            default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp(),
        )

    @declared_attr
    def updated_by(cls):
        return db.Column(
            db.String(50),
            default=lambda x: get_user().get("user_name", "UNKNOWN"),
            onupdate=lambda x: get_user().get("user_name", "UNKNOWN"),
        )

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<{self.__class__.__name__}: {getattr(self, inspect(self.__class__).primary_key[0].name)}>"

    @classmethod
    def find_one(cls, id, as_of_ts=None, *args, **kwargs) -> BaseModel:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get(
            "SUPPORT_TEMPORAL_TABLES", False
        )
        qry = cls.query
        if as_of_ts and SUPPORT_TEMPORAL_TABLES:
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")
        return qry.get(id)

    @classmethod
    def find_one_by_attr(
        cls, attrs: dict, as_of_ts=None, as_pandas=False, *args, **kwargs
    ) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get(
            "SUPPORT_TEMPORAL_TABLES", False
        )
        qry = cls.query.filter(*[getattr(cls, k) == v for k, v in attrs.items()])
        if as_of_ts and SUPPORT_TEMPORAL_TABLES:
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")

        if kwargs.get("last"):
            qry = qry.order_by(cls.created_dts.desc())

        if as_pandas:
            return pd.read_sql(
                qry.statement, qry.session.bind, coerce_float=False
            ).iloc[0]
        return qry.first()

    @classmethod
    def find_all_by_attr(
        cls, attrs: dict, as_of_ts=None, as_pandas=False, *args, **kwargs
    ) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get(
            "SUPPORT_TEMPORAL_TABLES", False
        )
        qry = cls.query.filter(
            *[
                getattr(cls, k).in_(v) if isinstance(v, list) else getattr(cls, k) == v
                for k, v in attrs.items()
            ]
        )
        if as_of_ts and SUPPORT_TEMPORAL_TABLES:
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")

        if as_pandas:
            return pd.read_sql(qry.statement, qry.session.bind, coerce_float=False)
        return qry.all()

    @classmethod
    def find_all(
        cls, limit=1000, offset=0, as_of_ts=None, as_pandas=False, *args, **kwargs
    ) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get(
            "SUPPORT_TEMPORAL_TABLES", False
        )
        qry = cls.query
        if as_of_ts and SUPPORT_TEMPORAL_TABLES:
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")
        if as_pandas:
            return pd.read_sql(
                qry.slice(offset, offset + limit).statement,
                qry.session.bind,
                coerce_float=False,
            )
        return qry.slice(offset, offset + limit).all()

    @classmethod
    def save_all_to_db(cls, data) -> None:
        try:
            db.session.add_all(data)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def update_one(cls, id: int, attrs: dict, *args, **kwargs) -> List[BaseModel]:
        if attrs.get("version_id") is None:
            raise ValueError("Must pass version_id when updating an existing record")
        pk = inspect(cls).primary_key[0]
        _ = attrs.pop(pk.name, None)
        version_id = attrs.pop("version_id")
        rows_updated = cls.query.filter(pk == id, cls.version_id == version_id).update(
            attrs, synchronize_session="fetch"
        )

        if rows_updated == 1:
            db.session.commit()
            return cls.query.get(id)

        db.session.rollback()

        # check if key exists, but version has changed
        id_exists = cls.query.filter(pk == id).count()
        if id_exists > 0:
            raise ExpiredRowVersionError(
                "This record has already been changed. Please refresh your data and try your request again"
            )

        raise ValueError("Record does not exist")

    @classmethod
    def replace_one(cls, id: int, attrs: dict, *args, **kwargs) -> List[BaseModel]:
        if attrs.get("version_id") is None:
            raise ValueError("Must pass version_id when updating an existing record")
        pk = inspect(cls).primary_key[0]
        payload_id = attrs.pop(pk.name, None)
        if payload_id != id:
            raise ValueError("Id of request and id in payload do not equal.")

        version_id = attrs.pop("version_id")
        rows_updated = cls.query.filter(pk == id, cls.version_id == version_id).update(
            attrs, synchronize_session="fetch"
        )
        if rows_updated == 1:
            db.session.commit()
            return cls.query.get(id)

        db.session.rollback()
        # check if key exists, but version has changed
        id_exists = cls.query.filter(pk == id).count()
        if id_exists > 0:
            raise ExpiredRowVersionError(
                "This record has already been changed. Please refresh your data and try your request again"
            )

        raise ValueError("Record does not exist")

    @classmethod
    def bulk_save_all_to_db(cls, data) -> None:
        try:
            db.session.bulk_save_objects(data)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


class BaseRuleModel(BaseModel):
    __abstract__ = True

    def nested_getattr(self, obj, nested_attr):
        """
        Returns a deeply nested relationship expressed as a string with dot notation.

        An example, `plan.group.group_label`, will return the group_label attribute from the
        group class from the plan class.
        """
        _attrs = nested_attr.split(".")
        return reduce(lambda o, next_attr: getattr(o, next_attr, None), _attrs, obj)


class BaseRowLevelSecurityTable:
    RLS_RESTRICTED_ROLE = "rls_restricted"
    RLS_SCHEMA = os.getenv("ROW_LEVEL_SECURITY_DB_SCHEMA", "rls")
    FN_NAME = "fn_rls__standard"

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def create_standard_policy(cls):
        sql = f"""
            SELECT COUNT(1)
            FROM   sys.objects
            WHERE  object_id = OBJECT_ID(N'{cls.RLS_SCHEMA}.{cls.FN_NAME}')
            AND type IN ( N'FN', N'IF', N'TF', N'FS', N'FT' )
        """

        rls_function_exists = db.session.execute(text_sql(sql)).fetchone()[0]
        if rls_function_exists != 0:
            return

        sql = f"""
            CREATE FUNCTION {cls.RLS_SCHEMA}.{cls.FN_NAME}(@user_role VARCHAR(30))
                RETURNS TABLE
            WITH SCHEMABINDING
            AS
            RETURN SELECT 1 AS {cls.FN_NAME}_output
            WHERE 
                COALESCE(IS_MEMBER('{cls.RLS_RESTRICTED_ROLE}'), 1) = 0 OR (
                    @user_role IN (
                        SELECT value AS user_role 
                        FROM STRING_SPLIT(CAST(SESSION_CONTEXT(N'user_roles') AS VARCHAR(8000)), ';')
                    )
                    OR 'superuser' IN (
                        SELECT value AS user_role 
                        FROM STRING_SPLIT(CAST(SESSION_CONTEXT(N'user_roles') AS VARCHAR(8000)), ';')
                    )
                )
        """
        db.session.execute(text_sql(sql))
        db.session.commit()

    @classmethod
    def add_rls(cls, model):
        table_schema = model.__table__.schema
        _schema = "dbo" if table_schema is None else f"{table_schema}"
        _tablename = model.__tablename__
        _policy_name = f"policy_rls__{_schema}_{_tablename}"

        cls.create_standard_policy()

        sql = f"""
            CREATE SECURITY POLICY {cls.RLS_SCHEMA}.{_policy_name}
            ADD FILTER PREDICATE {cls.RLS_SCHEMA}.{cls.FN_NAME}(auth_role_code) ON {_schema}.{_tablename}
            WITH (STATE = ON)
        """
        db.session.execute(text_sql(sql))
        db.session.commit()

    @classmethod
    def drop_rls(cls, model):
        table_schema = model.__table__.schema
        _schema = "dbo" if table_schema is None else f"{table_schema}"
        _tablename = model.__tablename__
        _policy_name = f"policy_rls__{_schema}_{_tablename}"

        sql = f"""
            DROP SECURITY POLICY {cls.RLS_SCHEMA}.{_policy_name};
        """
        try:
            db.session.execute(text_sql(sql))
            db.session.commit()
        except Exception:
            pass

        sql = f"""
            DROP FUNCTION {cls.RLS_SCHEMA}.{cls.FN_NAME};
        """
        try:
            db.session.execute(text_sql(sql))
            db.session.commit()
        except Exception:
            pass
