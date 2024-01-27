from . import (
    Config_AgeBand,
    Config_AgeDistribution,
    Config_AgeMapper,
    Config_AttributeDistribution,
    Config_AttributeSet,
    Config_Benefit,
    Config_BenefitDuration,
    Config_BenefitProductVariation,
    Config_BenefitProvision,
    Config_BenefitCovariance,
    Config_BenefitState,
    Config_Coverage,
    Config_Factor,
    Config_Product,
    Config_ProductMapper,
    Config_ProductState,
    Config_ProductVariation,
    Config_ProductVariationState,
    Config_Provision,
    Config_ProvisionState,
    Config_ProvisionUI,
    Config_RateGroup,
    Config_RateGroupFaceAmounts,
    Config_RateTable,
    Config_RelationshipMapper,
    Ref_AttrMapperType,
    Ref_Benefit,
    Ref_CensusStrategy,
    Ref_ComparisonOperator,
    Ref_DataTypes,
    Ref_InputType,
    Ref_Optionality,
    Ref_PremiumFrequency,
    Ref_ProductVariation,
    Ref_Provision,
    Ref_RatingStrategy,
    Ref_States,
    Ref_UnitType,
)


def load_refdata(hostname: str, *args, **kwargs):
    Ref_AttrMapperType.load(hostname, **kwargs)
    Ref_Benefit.load(hostname, **kwargs)
    Ref_CensusStrategy.load(hostname, **kwargs)
    Ref_ComparisonOperator.load(hostname, **kwargs)
    Ref_DataTypes.load(hostname, **kwargs)
    Ref_InputType.load(hostname, **kwargs)
    Ref_Optionality.load(hostname, **kwargs)
    Ref_PremiumFrequency.load(hostname, **kwargs)
    Ref_ProductVariation.load(hostname, **kwargs)
    Ref_Provision.load(hostname, **kwargs)
    Ref_RatingStrategy.load(hostname, **kwargs)
    Ref_States.load(hostname, **kwargs)
    Ref_UnitType.load(hostname, **kwargs)


def load_config(hostname: str, *args, **kwargs):
    Config_AgeBand.load(hostname, **kwargs)
    Config_AgeDistribution.load(hostname, **kwargs)
    Config_AttributeSet.load(hostname, **kwargs)
    Config_AttributeDistribution.load(hostname, **kwargs)

    Config_Product.load(hostname, **kwargs)
    Config_Coverage.load(hostname, **kwargs)
    Config_RateGroup.load(hostname, **kwargs)
    Config_RateGroupFaceAmounts.load(hostname, **kwargs)
    Config_AgeMapper.load(hostname, **kwargs)
    Config_ProductMapper.load(hostname, **kwargs)
    Config_RelationshipMapper.load(hostname, **kwargs)
    Config_ProductState.load(hostname, **kwargs)

    Config_ProductVariation.load(hostname, **kwargs)
    Config_ProductVariationState.load(hostname, **kwargs)

    Config_Benefit.load(hostname, **kwargs)
    Config_BenefitDuration.load(hostname, **kwargs)
    Config_BenefitState.load(hostname, **kwargs)

    Config_Provision.load(hostname, **kwargs)
    Config_ProvisionState.load(hostname, **kwargs)
    Config_ProvisionUI.load(hostname, **kwargs)
    Config_Factor.load(hostname, **kwargs)

    Config_BenefitProductVariation.load(hostname, **kwargs)
    Config_BenefitProvision.load(hostname, **kwargs)
    Config_BenefitCovariance.load(hostname, **kwargs)


def load_rate_table(hostname: str, *args, **kwargs):
    Config_RateTable.load(hostname, **kwargs)
