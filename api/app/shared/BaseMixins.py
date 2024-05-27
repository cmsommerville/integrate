from functools import reduce


class BaseRuleMixin:
    __abstract__ = True

    def nested_getattr(self, obj, nested_attr):
        """
        Returns a deeply nested relationship expressed as a string with dot notation.

        An example, `plan.group.group_label`, will return the group_label attribute from the
        group class from the plan class.
        """
        _attrs = nested_attr.split(".")
        return reduce(lambda o, next_attr: getattr(o, next_attr, None), _attrs, obj)
