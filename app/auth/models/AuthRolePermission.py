from app.extensions import db

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_PERMISSION = TBL_NAMES["AUTH_PERMISSION"]
AUTH_ROLE = TBL_NAMES["AUTH_ROLE"]
AUTH_ROLE_PERMISSION = TBL_NAMES["AUTH_ROLE_PERMISSION"]


class Model_AuthRolePermission(db.Model):
    __tablename__ = AUTH_ROLE_PERMISSION
    __table_args__ = (
        db.UniqueConstraint("auth_permission_id", "auth_role_id"),
        {"schema": SCHEMA_NAME},
    )

    auth_role_permission_id = db.Column(db.Integer, primary_key=True)
    auth_role_id = db.Column(db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_ROLE}.auth_role_id"))
    auth_permission_id = db.Column(
        db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_PERMISSION}.auth_permission_id")
    )

    permission = db.relationship("Model_AuthPermission", lazy="joined")

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<Model_AuthRolePermission: {self.auth_role_permission_id}>"

    @classmethod
    def find_one(cls, id, *args, **kwargs):
        return cls.query.get(id)

    @classmethod
    def find_by_role_id(cls, role_id, *args, **kwargs):
        return cls.query.filter(cls.auth_role_id == role_id).all()

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def save_all_to_db(self, objs) -> None:
        try:
            db.session.add_all(objs)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def delete(cls, roles):
        try:
            for role in roles:
                db.session.delete(role)
            db.session.commit()
        except:
            db.session.rollback()
            raise
