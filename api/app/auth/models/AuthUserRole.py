from app.extensions import db

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_ROLE = TBL_NAMES["AUTH_ROLE"]
AUTH_USER = TBL_NAMES["AUTH_USER"]
AUTH_USER_ROLE = TBL_NAMES["AUTH_USER_ROLE"]


class Model_AuthUserRole(db.Model):
    __tablename__ = AUTH_USER_ROLE
    __table_args__ = (
        db.UniqueConstraint("auth_user_id", "auth_role_id"),
        {"schema": SCHEMA_NAME},
    )

    auth_user_role_id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_USER}.auth_user_id"))
    auth_role_id = db.Column(db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_ROLE}.auth_role_id"))

    role = db.relationship("Model_AuthRole", lazy="joined")

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<Model_AuthUserRole: {self.auth_user_role_id}>"

    @classmethod
    def find_one(cls, id, *args, **kwargs):
        return cls.query.get(id)

    @classmethod
    def find_by_user_id(cls, user_id, *args, **kwargs):
        return cls.query.filter(cls.auth_user_id == user_id).all()

    def save_to_db(self) -> None:
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

    @classmethod
    def delete(cls, roles):
        try:
            for role in roles:
                db.session.delete(role)
            db.session.commit()
        except:
            db.session.rollback()
            raise
