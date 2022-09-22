from typing import List
from app.extensions import db
from app.shared import BaseModel

from ..tables import TBL_NAMES
from ..classes import RulesetApplicator
from .Config_Factor import Model_ConfigFactor
from .Config_RateTable import Model_ConfigRateTable
from .Selection_Benefit import Model_SelectionBenefit
from .Selection_Provision import Model_SelectionProvision
from .Config_BenefitProvision import Model_ConfigBenefitProvision

CONFIG_RATE_TABLE = TBL_NAMES['CONFIG_RATE_TABLE']
SELECTION_PROVISION = TBL_NAMES['SELECTION_PROVISION']
SELECTION_RATE_TABLE_FACTOR = TBL_NAMES['SELECTION_RATE_TABLE_FACTOR']



class Model_SelectionRateTableFactor(BaseModel):
    __tablename__ = SELECTION_RATE_TABLE_FACTOR

    selection_rate_table_factor_id = db.Column(db.Integer, primary_key=True)
    config_rate_table_id = db.Column(db.ForeignKey(f'{CONFIG_RATE_TABLE}.config_rate_table_id'))
    selection_provision_id = db.Column(db.ForeignKey(f'{SELECTION_PROVISION}.selection_provision_id'))
    selection_factor_value = db.Column(db.Numeric(8,5), default=1)
    
    config_rate_table = db.relationship("Model_ConfigRateTable")
    selection_provision = db.relationship("Model_SelectionProvision")

    @classmethod
    def find_selection_provisions(cls, selection_provision_ids: List[int], *args, **kwargs): 
        """
        Return query object containing the selection provisions. Must call the `all()` method to return the result set.
        """
        return cls.query.filter(cls.selection_provision_id.in_(selection_provision_ids))

    @classmethod
    def get_rate_table_factors(cls, selection_provision_ids: List[int], selection_plan_id: int):
        """
        Join rate table, selected benefits, and selected provisions by way of the configured benefit-provisions

        Returns a list of tuples of format: List[(<Config_RateTable>, <Selection_Benefit>, <Selection_Provision>)]
        """
        qry = db.session.query(Model_ConfigRateTable, Model_SelectionBenefit, Model_SelectionProvision)
        qry = qry.select_from(Model_ConfigRateTable)
        qry = qry.join(Model_SelectionBenefit, Model_ConfigRateTable.config_benefit_product_variation_id==Model_SelectionBenefit.config_benefit_product_variation_id)
        qry = qry.join(Model_ConfigBenefitProvision, Model_SelectionBenefit.config_benefit_id==Model_ConfigBenefitProvision.config_benefit_id)
        qry = qry.join(Model_SelectionProvision, Model_ConfigBenefitProvision.config_provision_id==Model_SelectionProvision.config_provision_id)
        qry = qry.filter(
            Model_SelectionProvision.selection_provision_id.in_(selection_provision_ids), 
            Model_SelectionBenefit.selection_plan_id==selection_plan_id, 
        )
        return qry.all()
