from typing import List
from app.extensions import db

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_ROLE = TBL_NAMES["AUTH_ROLE"]


class Model_AuthRole(db.Model):
    __tablename__ = AUTH_ROLE
    __table_args__ = (
        db.UniqueConstraint("auth_role_code"),
        {"schema": SCHEMA_NAME},
    )

    auth_role_id = db.Column(db.Integer, primary_key=True)
    auth_role_code = db.Column(db.String(30), nullable=False)
    auth_role_label = db.Column(db.String(100), nullable=False)
    auth_role_description = db.Column(db.String(1000))

    permissions = db.relationship(
        "Model_AuthRolePermission",
        lazy="joined",
    )

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<Model_AuthRole: {self.auth_role_id}>"

    @classmethod
    def find_all(cls, *args, **kwargs):
        qry = cls.query
        return qry.all()

    @classmethod
    def find_one(cls, id, *args, **kwargs):
        qry = cls.query
        return qry.get(id)

    @classmethod
    def find_by_code(cls, auth_role_codes: List[str], *args, **kwargs):
        return cls.query.filter(cls.auth_role_code.in_(auth_role_codes)).all()

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
