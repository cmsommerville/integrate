from __future__ import annotations
import pandas as pd
from functools import reduce
from flask import current_app
from typing import List
from sqlalchemy import text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def created_dts(cls):
        return db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    @declared_attr
    def updated_dts(cls):
        return db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @declared_attr
    def updated_by(cls):
        return db.Column(db.String(50))

    def __repr__(self): 
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f'<{self.__class__.__name__}: {getattr(self, inspect(self.__class__).primary_key[0].name)}>'


    @classmethod
    def find_one(cls, id, as_of_ts=None, *args, **kwargs) -> BaseModel:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get("SUPPORT_TEMPORAL_TABLES", False)
        qry = cls.query
        if as_of_ts and SUPPORT_TEMPORAL_TABLES: 
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")
        return qry.get(id)

    @classmethod
    def find_one_by_attr(cls, attrs: dict, as_of_ts=None, *args, **kwargs) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get("SUPPORT_TEMPORAL_TABLES", False)
        qry = cls.query.filter(*[getattr(cls, k) == v for k, v in attrs.items()])
        if as_of_ts and SUPPORT_TEMPORAL_TABLES: 
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")

        if kwargs.get('last'): 
            return qry.order_by(cls.created_dts.desc()).first()
        return qry.first()

    @classmethod
    def find_all_by_attr(cls, attrs: dict, as_of_ts=None, *args, **kwargs) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get("SUPPORT_TEMPORAL_TABLES", False)
        qry = cls.query.filter(*[getattr(cls, k) == v for k, v in attrs.items()])
        if as_of_ts and SUPPORT_TEMPORAL_TABLES: 
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")
        return qry.all()

    @classmethod
    def find_all(cls, limit=1000, offset=0, as_of_ts=None, *args, **kwargs) -> List[BaseModel]:
        SUPPORT_TEMPORAL_TABLES = current_app.config.get("SUPPORT_TEMPORAL_TABLES", False)
        qry = cls.query
        if as_of_ts and SUPPORT_TEMPORAL_TABLES: 
            qry = qry.with_hint(cls, f"FOR SYSTEM_TIME AS OF '{as_of_ts}'")
        return qry.slice(offset, offset+limit).all()

    @classmethod
    def save_all_to_db(cls, data) -> None:
        try:
            db.session.add_all(data)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

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
        _attrs = nested_attr.split('.')
        return reduce(lambda o, next_attr: getattr(o, next_attr, None), _attrs, obj)
