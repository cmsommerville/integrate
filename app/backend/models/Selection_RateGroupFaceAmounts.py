import pandas as pd
from app.backend.models.Config_AttributeDetail import CONFIG_ATTRIBUTE_DETAIL
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_ATTRIBUTE_DETAIL = TBL_NAMES['CONFIG_ATTRIBUTE_DETAIL']
CONFIG_RATE_GROUP = TBL_NAMES['CONFIG_RATE_GROUP']
CONFIG_RATE_GROUP_FACE_AMOUNTS = TBL_NAMES['CONFIG_RATE_GROUP_FACE_AMOUNTS']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']
SELECTION_RATE_GROUP_FACE_AMOUNTS = TBL_NAMES['SELECTION_RATE_GROUP_FACE_AMOUNTS']

class Model_SelectionRateGroupFaceAmounts(BaseModel):
    __tablename__ = SELECTION_RATE_GROUP_FACE_AMOUNTS
    __table_args__ = (
        db.UniqueConstraint('selection_plan_id', 'config_rate_group_id', 
        'config_gender_detail_id', 'config_smoker_status_detail_id', 
        'config_relationship_detail_id', 'face_amount_value'), 
    )

    selection_rate_group_face_amount_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(F"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    config_rate_group_id = db.Column(db.ForeignKey(F"{CONFIG_RATE_GROUP}.config_rate_group_id"), nullable=False)
    config_gender_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_smoker_status_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_relationship_detail_id = db.Column(db.ForeignKey(F"{CONFIG_ATTRIBUTE_DETAIL}.config_attr_detail_id"), nullable=False)
    config_rate_group_face_amount_id = db.Column(db.ForeignKey(F"{CONFIG_RATE_GROUP_FACE_AMOUNTS}.config_rate_group_face_amount_id"))
    face_amount_value = db.Column(db.Numeric(10, 2), nullable=False)

    @classmethod
    def find_by_plan(cls, plan_id: int, as_pandas=False, *args, **kwargs):
        qry = cls.query.filter(cls.selection_plan_id == plan_id)
        if as_pandas: 
            return pd.read_sql(qry.statement, qry.session.bind, coerce_float=False)
        return qry.all()

    @classmethod
    def delete_by_plan(cls, plan_id: int, *args, **kwargs):
        try: 
            cls.query.filter(cls.selection_plan_id==plan_id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise