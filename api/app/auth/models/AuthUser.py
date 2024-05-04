from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_USER = TBL_NAMES["AUTH_USER"]
AUTH_USER_PASSWORD_HISTORY = TBL_NAMES["AUTH_USER_PASSWORD_HISTORY"]


class Model_AuthUserPasswordHistory(db.Model):
    __tablename__ = AUTH_USER_PASSWORD_HISTORY
    __table_args__ = {"schema": SCHEMA_NAME}

    auth_user_password_history_id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_USER}.auth_user_id"),
        nullable=False,
    )
    hashed_password = db.Column(db.LargeBinary, nullable=False)
    created_dts = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )


class Model_AuthUser(db.Model):
    __tablename__ = AUTH_USER
    __table_args__ = (db.UniqueConstraint("user_name"), {"schema": SCHEMA_NAME})

    auth_user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.LargeBinary, nullable=False)
    password_last_changed_dt = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    manager_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{SCHEMA_NAME}.{AUTH_USER}.auth_user_id"),
        nullable=True,
    )

    roles = db.relationship("Model_AuthUserRole")
    password_history = db.relationship(
        "Model_AuthUserPasswordHistory",
        order_by="desc(Model_AuthUserPasswordHistory.created_dts)",
    )

    @hybrid_property
    def password_list(self):
        return [pw.hashed_password for pw in self.password_history][:5]

    def get_direct_reports(self):
        """
        Return a list of direct reports for the user. This list includes the user herself.
        """
        beginning_getter = (
            db.session.query(Model_AuthUser)
            .filter(Model_AuthUser.auth_user_id == self.auth_user_id)
            .cte(name="children_for", recursive=True)
        )
        with_recursive = beginning_getter.union_all(
            db.session.query(Model_AuthUser).filter(
                Model_AuthUser.manager_id == beginning_getter.c.auth_user_id
            )
        )
        return db.session.query(with_recursive).all()

    def __repr__(self):
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f"<Model_AuthUser: {self.auth_user_id}>"

    @classmethod
    def get_id(cls):
        return str(cls.auth_user_id)

    @classmethod
    def find_one(cls, id, *args, **kwargs) -> db.Model:
        qry = cls.query
        return qry.get(id)

    @classmethod
    def find_by_user_name(cls, user_name, *args, **kwargs) -> db.Model:
        return cls.query.filter(cls.user_name == user_name).first()

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
