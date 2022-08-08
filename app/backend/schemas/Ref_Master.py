from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_RefComparisonOperator, Model_RefComponentTypes, \
    Model_RefOptionality, Model_RefInputTypes, Model_RefUnitCode, Model_RefPremiumFrequency, \
    Model_RefBenefit, Model_RefProvision


class Schema_RefBenefit(BaseSchema):
    class Meta:
        model = Model_RefBenefit
        load_instance = True

    ref_entity_code = ma.Constant('benefit')
    ref_id = ma.Integer(data_key="ref_benefit_id")
    ref_attr_code = ma.String(data_key="ref_benefit_code")
    ref_attr_label = ma.String(data_key="ref_benefit_label")
    ref_attr_description = ma.String(data_key="ref_benefit_description")
    

class Schema_RefProvision(BaseSchema):
    class Meta:
        model = Model_RefProvision
        load_instance = True

    ref_entity_code = ma.Constant('provision')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()
    

class Schema_RefPremiumFrequency(BaseSchema):
    class Meta:
        model = Model_RefPremiumFrequency
        load_instance = True

    ref_entity_code = ma.Constant('premium_frequency')
    ref_id = ma.Integer(data_key="premium_frequency_id")
    ref_attr_code = ma.String(data_key="premium_frequency_code")
    ref_attr_label = ma.String(data_key="premium_frequency_label")
    ref_attr_description = ma.String(data_key="premium_frequency_description")
    ref_attr_symbol = ma.String(data_key="premium_frequency_symbol")
    ref_attr_value = ma.Float(data_key="premium_frequency_value")

class Schema_RefComparisonOperator(BaseSchema):
    class Meta:
        model = Model_RefComparisonOperator
        load_instance = True

    ref_entity_code = ma.Constant('comparison_operator')
    ref_id = ma.Integer(data_key="comparison_operator_id")
    ref_attr_code = ma.String(data_key="comparison_operator_code")
    ref_attr_label = ma.String(data_key="comparison_operator_label")
    ref_attr_description = ma.String(data_key="comparison_operator_description")
    ref_attr_symbol = ma.String(data_key="comparison_operator_symbol")
    ref_attr_value = ma.Float(data_key="comparison_operator_value")
    