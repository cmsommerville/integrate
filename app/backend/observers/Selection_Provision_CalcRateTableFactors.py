from typing import Union, List
from app.shared import BaseObserver
from app.extensions import db

from ..classes import RulesetApplicator
from ..models import Model_SelectionProvision, Model_SelectionRateTableFactor
from ..observables import Observable_SelectionProvision

class Observer_SelectionProvision_CalcRateTableFactors(BaseObserver):

    def __init__(self):
        pass

    def subscribe(self): 
        Observable_SelectionProvision.subscribe(self)

    def _delete_handler(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]], *args, **kwargs):
        if type(provisions) != list: 
            provisions = [provisions]
            
        rtfs = Model_SelectionRateTableFactor.find_selection_provisions([prov.selection_provision_id for prov in provisions])
        rtfs.delete()
        try: 
            db.session.commit()
        except: 
            db.session.rollback()


    def _change_handler(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]]):
        if type(provisions) != list: 
            provisions = [provisions]

        provision_ids = [prov.selection_provision_id for prov in provisions if prov.config_provision.config_provision_type_code == 'rate_table']
        plan_id = provisions[0].selection_plan_id
        rtfs = Model_SelectionRateTableFactor.get_rate_table_factors(provision_ids, plan_id)
        rate_table_factors = []

        ruleset_applicators = [
            RulesetApplicator(attrs={
                'rate_table': rt, 
                'benefit': bnft, 
                'provision': prov, 
            })
            for (rt, bnft, prov) in rtfs
        ]
        for applicator in ruleset_applicators: 
            if applicator.provision.is_product_factor:
                continue

            # get factor rulesets
            rulesets = applicator.provision.config_provision.factors
            # apply all the rulesets and return the first true ruleset
            factor = applicator.apply_rulesets(rulesets)

            selection_rate_table_factor = Model_SelectionRateTableFactor(**{
                'config_rate_table_id': applicator.rate_table.config_rate_table_id, 
                'selection_provision_id': applicator.provision.selection_provision_id, 
                'selection_factor_value': factor.factor_value if factor else 1, 
            })

            # get the factor value
            rate_table_factors.append(selection_rate_table_factor)

        Model_SelectionRateTableFactor.bulk_save_all_to_db(rate_table_factors)

    def post(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]], *args, **kwargs):
        print("In Observer_SelectionProvision_CalcRateTableFactors...")
        self._change_handler(provisions)

    def put(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]], *args, **kwargs):
        print("In Observer_SelectionProvision_CalcRateTableFactors...")
        self._change_handler(provisions)

    def patch(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]], *args, **kwargs):
        print("In Observer_SelectionProvision_CalcRateTableFactors...")
        self._change_handler(provisions)

    def delete(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]], *args, **kwargs):
        print("In Observer_SelectionProvision_CalcRateTableFactors...")
        self._delete_handler(provisions)
    
observer_selection_provision_calc_rate_table_factors = Observer_SelectionProvision_CalcRateTableFactors()