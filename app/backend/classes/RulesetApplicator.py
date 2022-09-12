from typing import Dict, List
from app.shared import BaseRuleset

class RulesetApplicator:

    def __init__(self, *args, **kwargs):
        if kwargs.get('attrs'): 
            self.set(kwargs.get('attrs'))

    def set(self, attrs: Dict[str, BaseRuleset], *args, **kwargs):
        """
        Provide a dictionary of root level models against which rules will be applied
        """
        for key, model in attrs.items():
            setattr(self, key, model)

    def apply_rulesets(self, rulesets: List[BaseRuleset], *args, **kwargs): 
        self._ruleset = next((ruleset for ruleset in rulesets if ruleset.apply_ruleset(self)),  None)
        return self._ruleset
