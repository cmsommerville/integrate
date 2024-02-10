from typing import List
from app.extensions import db

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_PERMISSION = TBL_NAMES["AUTH_PERMISSION"]


class Model_AuthPermission(db.Model):
    __tablename__ = AUTH_PERMISSION
    __table_args__ = (
        db.UniqueConstraint("auth_permission_code"),
        {"schema": SCHEMA_NAME},
    )

    auth_permission_id = db.Column(db.Integer, primary_key=True)
    auth_permission_code = db.Column(db.String(30), nullable=False)
    auth_permission_description = db.Column(db.String(1000))

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<Model_AuthPermission: {self.auth_permission_id}>"

    @classmethod
    def find_all(cls, *args, **kwargs):
        qry = cls.query
        return qry.all()

    @classmethod
    def find_one(cls, id, *args, **kwargs):
        qry = cls.query
        return qry.get(id)

    @classmethod
    def find_by_code(cls, codes: List[str], *args, **kwargs):
        return cls.query.filter(cls.auth_permission_code.in_(codes)).all()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def save_all_to_db(self, objs):
        try:
            db.session.add_all(objs)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
