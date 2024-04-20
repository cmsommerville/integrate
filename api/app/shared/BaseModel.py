from __future__ import annotations
from ulid import ULID
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.mssql import DATETIME2
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

    @declared_attr
    def row_eff_dts(cls):
        return db.Column(DATETIME2, nullable=False)

    @declared_attr
    def row_exp_dts(cls):
        return db.Column(DATETIME2, nullable=False)

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<{self.__class__.__name__}: {getattr(self, inspect(self.__class__).primary_key[0].name)}>"

    @classmethod
    def find_one(cls, id, parent_id=None, *args, **kwargs) -> BaseModel:
        pk = inspect(cls).primary_key[0]
        qry = cls.query
        if parent_id is not None and cls.parent is not None:
            parent_id_col = inspect(cls.parent.property.entity).primary_key[0]
            qry = qry.options(joinedload(cls.parent)).filter(parent_id_col == parent_id)
        return qry.filter(pk == id).one_or_none()

    @classmethod
    def find_by_parent(
        cls, parent_id, limit=1000, offset=0, *args, **kwargs
    ) -> List[BaseModel]:
        if cls.parent is None:
            raise ValueError("This model does not have a parent relationship")

        parent_id_col = inspect(cls.parent.property.entity).primary_key[0]
        qry = (
            cls.query.options(joinedload(cls.parent))
            .filter(parent_id_col == parent_id)
            .slice(offset, offset + limit)
        )
        return qry.all()

    @classmethod
    def find_one_by_attr(cls, attrs: dict, *args, **kwargs) -> List[BaseModel]:
        qry = cls.query.filter(*[getattr(cls, k) == v for k, v in attrs.items()])

        if kwargs.get("last"):
            qry = qry.order_by(cls.created_dts.desc())

        return qry.first()

    @classmethod
    def find_all_by_attr(cls, attrs: dict, *args, **kwargs) -> List[BaseModel]:
        return cls.query.filter(
            *[
                getattr(cls, k).in_(v) if isinstance(v, list) else getattr(cls, k) == v
                for k, v in attrs.items()
            ]
        ).all()

    @classmethod
    def find_all(cls, limit=1000, offset=0, *args, **kwargs) -> List[BaseModel]:
        return cls.query.slice(offset, offset + limit).all()

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
