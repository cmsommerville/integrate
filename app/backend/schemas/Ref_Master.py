from app.extensions import ma
from app.shared import BaseSchema

from .. import models


class Schema_RefAttrMapperType(BaseSchema):
    class Meta:
        model = models.Model_RefAttrMapperType
        load_instance = True

    ref_entity_code = ma.Constant('attr_type_code')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefBenefit(BaseSchema):
    class Meta:
        model = models.Model_RefBenefit
        load_instance = True

    ref_entity_code = ma.Constant('benefit')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefCensusStrategy(BaseSchema):
    class Meta:
        model = models.Model_RefCensusStrategy
        load_instance = True

    ref_entity_code = ma.Constant('census_strategy')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefComparisonOperator(BaseSchema):
    class Meta:
        model = models.Model_RefComparisonOperator
        load_instance = True

    ref_entity_code = ma.Constant('comparison_operator')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefComponentTypes(BaseSchema):
    class Meta:
        model = models.Model_RefComponentTypes
        load_instance = True

    ref_entity_code = ma.Constant('component_type')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefDataTypes(BaseSchema):
    class Meta:
        model = models.Model_RefDataTypes
        load_instance = True

    ref_entity_code = ma.Constant('data_type')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefFactorType(BaseSchema):
    class Meta:
        model = models.Model_RefFactorType
        load_instance = True

    ref_entity_code = ma.Constant('factor_type')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefInputTypes(BaseSchema):
    class Meta:
        model = models.Model_RefInputTypes
        load_instance = True

    ref_entity_code = ma.Constant('input_type')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefOptionality(BaseSchema):
    class Meta:
        model = models.Model_RefOptionality
        load_instance = True

    ref_entity_code = ma.Constant('optionality')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefPremiumFrequency(BaseSchema):
    class Meta:
        model = models.Model_RefPremiumFrequency
        load_instance = True

    ref_entity_code = ma.Constant('premium_frequency')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefProductVariation(BaseSchema):
    class Meta:
        model = models.Model_RefProductVariation
        load_instance = True

    ref_entity_code = ma.Constant('product_variation')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefProvision(BaseSchema):
    class Meta:
        model = models.Model_RefProvision
        load_instance = True

    ref_entity_code = ma.Constant('provision')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefRatingStrategy(BaseSchema):
    class Meta:
        model = models.Model_RefRatingStrategy
        load_instance = True

    ref_entity_code = ma.Constant('rating_strategy')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()

class Schema_RefUnitCode(BaseSchema):
    class Meta:
        model = models.Model_RefUnitCode
        load_instance = True

    ref_entity_code = ma.Constant('unit_code')
    ref_id = ma.Integer()
    ref_attr_code = ma.String()
    ref_attr_label = ma.String()
    ref_attr_description = ma.String()
