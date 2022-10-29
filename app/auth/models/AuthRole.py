from app.extensions import db

from ..tables import TBL_NAMES

AUTH_ROLE = TBL_NAMES['AUTH_ROLE']
AUTH_USER = TBL_NAMES['AUTH_USER']

class Model_AuthRole(db.Model):
    __tablename__ = AUTH_ROLE
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_name'),
    )

    role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(f"{AUTH_USER}.user_id"))
    role_name = db.Column(db.String(200), nullable=False)

    def __repr__(self): 
        """
        Print instance as <[Model Name]: [Row SK]>
        """
        return f'<Model_AuthRole: {self.role_id}>'


    @classmethod
    def find_one(cls, id, *args, **kwargs) -> db.Model:
        return cls.query.get(id)

    @classmethod
    def find_by_user_id(cls, user_id, *args, **kwargs) -> db.Model:
        return cls.query.filter(cls.user_id==user_id).all()

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
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


