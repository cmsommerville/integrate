from typing import Union, List
from app.shared import BaseObserver

from ..classes import RulesetApplicator
from ..models import Model_SelectionProvision
from ..observables import Observable_SelectionProvision

class Observer_SelectionProvision_CalcProductFactors(BaseObserver):

    def __init__(self):
        pass

    def subscribe(self): 
        Observable_SelectionProvision.subscribe(self)

    def get(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]]):
        print("In Observer_SelectionProvision_CalcProductFactors...")

    def post(self, provisions: Union[Model_SelectionProvision, List[Model_SelectionProvision]]):
        print("In Observer_SelectionProvision_CalcProductFactors...")
        product_factors = []
        if type(provisions) != list: 
            provisions = [provisions]

        for prov in provisions: 
            if not prov.is_product_factor:
                continue

            # create a ruleset applicator object to call the apply rule(set) methods
            ruleset_applicator = RulesetApplicator(attrs={'provision': prov})
            # apply all the rulesets and return the first true ruleset
            factor = ruleset_applicator.apply_rulesets(prov.config_provision.factors)
            # get the factor value
            prov.selection_factor_value = getattr(factor, 'factor_value')
            product_factors.append(prov)

        Model_SelectionProvision.save_all_to_db(product_factors)


observer_selection_provision_calc_product_factors = Observer_SelectionProvision_CalcProductFactors()
