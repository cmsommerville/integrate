from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_SelectionPlan, Model_SelectionPlan_ACL
from .Selection_Coverage import Schema_SelectionCoverage


class Schema_SelectionPlan_ACL(BaseSchema):
    class Meta:
        model = Model_SelectionPlan_ACL
        load_instance = True
        include_fk = True


class Schema_SelectionPlan(BaseSchema):
    class Meta:
        model = Model_SelectionPlan
        load_instance = True
        include_fk = True

    coverages = ma.Nested("Schema_SelectionCoverage", many=True)
    acl = ma.Nested("Schema_SelectionPlan_ACL", many=True, load_only=True)
    # coverages = ma.Method("get_coverages", deserialize="load_coverages")

    def get_acl(self, obj, *args, **kwargs):
        return Schema_SelectionPlan_ACL(context=self.context).dump(
            obj.get_acl(**self.context), many=True
        )

    def load_acl(self, value, *args, **kwargs):
        return [Schema_SelectionPlan_ACL(context=self.context).load(v) for v in value]

    def get_coverages(self, obj, *args, **kwargs):
        return Schema_SelectionCoverage(context=self.context).dump(
            obj.get_coverages(context=self.context, **self.context), many=True
        )

    def load_coverages(self, value, *args, **kwargs):
        return [Schema_SelectionCoverage(context=self.context).load(v) for v in value]
