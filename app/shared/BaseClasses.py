from functools import reduce

class BaseRuleset():

    def apply_ruleset(self):
        pass


class BaseRule():

    def apply_rule(self):
        pass

    def nested_getattr(self, obj, nested_attr):
        """
        Returns a deeply nested relationship expressed as a string with dot notation.

        An example, `plan.group.group_label`, will return the group_label attribute from the 
        group class from the plan class.
        """
        _attrs = nested_attr.split('.')
        return reduce(lambda o, next_attr: getattr(o, next_attr, None), _attrs, obj)


