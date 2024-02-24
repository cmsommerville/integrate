from app.extensions import db

from ..tables import TBL_NAMES, SCHEMA_NAME

AUTH_USER = TBL_NAMES['AUTH_USER']

class Model_AuthUser(db.Model):
    __tablename__ = AUTH_USER
    __table_args__ = (
        db.UniqueConstraint('user_name'),
        {"schema": SCHEMA_NAME}
    )

    auth_user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.LargeBinary, nullable=False)

    roles = db.relationship("Model_AuthUserRole")

    def __repr__(self): 
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f'<Model_AuthUser: {self.auth_user_id}>'

    @classmethod
    def get_id(cls): 
        return str(cls.auth_user_id)
    
    @classmethod
    def find_one(cls, id, *args, **kwargs) -> db.Model:
        qry = cls.query
        return qry.get(id)

    @classmethod
    def find_by_user_name(cls, user_name, *args, **kwargs) -> db.Model:
        return cls.query.filter(cls.user_name==user_name).first()

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
