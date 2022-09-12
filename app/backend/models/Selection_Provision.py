import datetime
from typing import List
from app.extensions import db
from app.shared import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property

from ..tables import TBL_NAMES

CONFIG_BENEFIT_PROVISION = TBL_NAMES['CONFIG_BENEFIT_PROVISION']
CONFIG_PROVISION = TBL_NAMES['CONFIG_PROVISION']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_PLAN = TBL_NAMES['SELECTION_PLAN']

class Model_SelectionProvision(BaseModel):
    __tablename__ = SELECTION_PROVISION
    __table_args__ = (
        db.UniqueConstraint('selection_plan_id', 'config_provision_id', ), 
    )

    selection_provision_id = db.Column(db.Integer, primary_key=True)
    selection_plan_id = db.Column(db.ForeignKey(f"{SELECTION_PLAN}.selection_plan_id"), nullable=False)
    config_provision_id = db.Column(db.ForeignKey(f"{CONFIG_PROVISION}.config_provision_id"), nullable=False)
    selection_provision_value = db.Column(db.String(255), nullable=False)
    selection_factor_value = db.Column(db.Numeric(8,5), nullable=True)

    config_provision = db.relationship("Model_ConfigProvision", lazy='joined')

    @hybrid_property
    def selection_value(self): 
        prov = getattr(self, 'config_provision', None)
        data_type_obj = getattr(prov, 'data_type', None)
        data_type = getattr(data_type_obj, 'ref_attr_code', None)
        if data_type in ['number', 'int', 'float']:
            return float(self.selection_provision_value)
        if data_type in ['bool', 'boolean']: 
            return self.selection_provision_value.upper() == 'TRUE'
        return self.selection_provision_value
        
    @hybrid_property
    def is_product_factor(self):
        return self.config_provision.config_provision_type_code == 'product'