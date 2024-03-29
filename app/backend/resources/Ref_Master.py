import pandas as pd
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from .. import models
from .. import schemas


class CRUD_RefAttrMapperType(BaseCRUDResource):
    model = models.Model_RefAttrMapperType
    schema = schemas.Schema_RefAttrMapperType()


class CRUD_RefAttrMapperType_List(BaseCRUDResourceList):
    model = models.Model_RefAttrMapperType
    schema = schemas.Schema_RefAttrMapperType(many=True)


class CRUD_RefBenefit(BaseCRUDResource):
    model = models.Model_RefBenefit
    schema = schemas.Schema_RefBenefit()


class CRUD_RefBenefit_List(BaseCRUDResourceList):
    model = models.Model_RefBenefit
    schema = schemas.Schema_RefBenefit(many=True)


class CRUD_RefCensusStrategy(BaseCRUDResource):
    model = models.Model_RefCensusStrategy
    schema = schemas.Schema_RefCensusStrategy()


class CRUD_RefCensusStrategy_List(BaseCRUDResourceList):
    model = models.Model_RefCensusStrategy
    schema = schemas.Schema_RefCensusStrategy(many=True)


class CRUD_RefComparisonOperator(BaseCRUDResource):
    model = models.Model_RefComparisonOperator
    schema = schemas.Schema_RefComparisonOperator()


class CRUD_RefComparisonOperator_List(BaseCRUDResourceList):
    model = models.Model_RefComparisonOperator
    schema = schemas.Schema_RefComparisonOperator(many=True)


class CRUD_RefComponentTypes(BaseCRUDResource):
    model = models.Model_RefComponentTypes
    schema = schemas.Schema_RefComponentTypes()


class CRUD_RefComponentTypes_List(BaseCRUDResourceList):
    model = models.Model_RefComponentTypes
    schema = schemas.Schema_RefComponentTypes(many=True)


class CRUD_RefDataTypes(BaseCRUDResource):
    model = models.Model_RefDataTypes
    schema = schemas.Schema_RefDataTypes()


class CRUD_RefDataTypes_List(BaseCRUDResourceList):
    model = models.Model_RefDataTypes
    schema = schemas.Schema_RefDataTypes(many=True)


class CRUD_RefFactorType(BaseCRUDResource):
    model = models.Model_RefFactorType
    schema = schemas.Schema_RefFactorType()


class CRUD_RefFactorType_List(BaseCRUDResourceList):
    model = models.Model_RefFactorType
    schema = schemas.Schema_RefFactorType(many=True)


class CRUD_RefInputTypes(BaseCRUDResource):
    model = models.Model_RefInputTypes
    schema = schemas.Schema_RefInputTypes()


class CRUD_RefInputTypes_List(BaseCRUDResourceList):
    model = models.Model_RefInputTypes
    schema = schemas.Schema_RefInputTypes(many=True)


class CRUD_RefOptionality(BaseCRUDResource):
    model = models.Model_RefOptionality
    schema = schemas.Schema_RefOptionality()


class CRUD_RefOptionality_List(BaseCRUDResourceList):
    model = models.Model_RefOptionality
    schema = schemas.Schema_RefOptionality(many=True)


class CRUD_RefPremiumFrequency(BaseCRUDResource):
    model = models.Model_RefPremiumFrequency
    schema = schemas.Schema_RefPremiumFrequency()


class CRUD_RefPremiumFrequency_List(BaseCRUDResourceList):
    model = models.Model_RefPremiumFrequency
    schema = schemas.Schema_RefPremiumFrequency(many=True)


class CRUD_RefProductVariation(BaseCRUDResource):
    model = models.Model_RefProductVariation
    schema = schemas.Schema_RefProductVariation()


class CRUD_RefProductVariation_List(BaseCRUDResourceList):
    model = models.Model_RefProductVariation
    schema = schemas.Schema_RefProductVariation(many=True)


class CRUD_RefProvision(BaseCRUDResource):
    model = models.Model_RefProvision
    schema = schemas.Schema_RefProvision()


class CRUD_RefProvision_List(BaseCRUDResourceList):
    model = models.Model_RefProvision
    schema = schemas.Schema_RefProvision(many=True)


class CRUD_RefRateFrequency(BaseCRUDResource):
    model = models.Model_RefRateFrequency
    schema = schemas.Schema_RefRateFrequency()


class CRUD_RefRateFrequency_List(BaseCRUDResourceList):
    model = models.Model_RefRateFrequency
    schema = schemas.Schema_RefRateFrequency(many=True)


class CRUD_RefRatingStrategy(BaseCRUDResource):
    model = models.Model_RefRatingStrategy
    schema = schemas.Schema_RefRatingStrategy()


class CRUD_RefRatingStrategy_List(BaseCRUDResourceList):
    model = models.Model_RefRatingStrategy
    schema = schemas.Schema_RefRatingStrategy(many=True)


class CRUD_RefUnitCode(BaseCRUDResource):
    model = models.Model_RefUnitCode
    schema = schemas.Schema_RefUnitCode()


class CRUD_RefUnitCode_List(BaseCRUDResourceList):
    model = models.Model_RefUnitCode
    schema = schemas.Schema_RefUnitCode(many=True)
