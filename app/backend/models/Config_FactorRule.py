from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES

CONFIG_FACTOR = TBL_NAMES['CONFIG_FACTOR']
CONFIG_FACTOR_RULE = TBL_NAMES['CONFIG_FACTOR_RULE']
REF_MASTER = TBL_NAMES['REF_MASTER']


class Model_ConfigFactorRule(BaseModel):
    __tablename__ = CONFIG_FACTOR_RULE

    config_factor_rule_id = db.Column(db.Integer, primary_key=True)
    config_factor_id = db.Column(db.ForeignKey(
        f"{CONFIG_FACTOR}.config_factor_id"
    ))
    comparison_class_name = db.Column(db.String(100), nullable=False, 
        comment="Class name of the model containing the column that is being compared")
    comparison_column_name = db.Column(db.String(100), nullable=False, 
        comment="Column name of the column that is being compared")
    comparison_operator_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"
    ), nullable=False, comment="Pythonic comparison operators, such as __eq__, __gt__, etc.")
    comparison_column_value = db.Column(db.String(100), nullable=False)
    comparison_column_data_type_id = db.Column(db.ForeignKey(
        f"{REF_MASTER}.ref_id"
    ), nullable=False, comment="Pythonic data types, such as str, float, etc.")