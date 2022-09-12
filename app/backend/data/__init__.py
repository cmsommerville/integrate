from . import Config_AgeBand, Config_AgeDistribution, Config_AgeMapper, \
    Config_AttributeDistribution, Config_AttributeSet, Config_Benefit, Config_BenefitDuration,\
    Config_BenefitProductVariation, Config_BenefitProvision, \
    Config_BenefitState, Config_Coverage, Config_Factor, Config_Product, Config_ProductMapper, \
    Config_ProductState, Config_ProductVariation, Config_ProductVariationState,\
    Config_Provision, Config_ProvisionState, Config_ProvisionUI, Config_RateGroup, \
    Config_RateTable, Config_RelationshipMapper, \
    Ref_AttrMapperType, Ref_Benefit,Ref_CensusStrategy, Ref_ComparisonOperator, Ref_DataTypes, \
    Ref_InputType, Ref_ProductVariation,Ref_Provision, Ref_RatingStrategy, Ref_States, Ref_UnitType, \
    Selection_AgeBand, Selection_Benefit, Selection_BenefitDuration, Selection_Plan, Selection_Provision


def load_refdata(hostname: str):
    Ref_AttrMapperType.load(hostname)
    Ref_Benefit.load(hostname)
    Ref_CensusStrategy.load(hostname)
    Ref_ComparisonOperator.load(hostname)
    Ref_DataTypes.load(hostname)
    Ref_InputType.load(hostname)
    Ref_ProductVariation.load(hostname)
    Ref_Provision.load(hostname)
    Ref_RatingStrategy.load(hostname)
    Ref_States.load(hostname)
    Ref_UnitType.load(hostname)


def load_config(hostname: str):
    Config_AgeBand.load(hostname)
    Config_AgeDistribution.load(hostname)
    Config_AttributeSet.load(hostname)
    Config_AttributeDistribution.load(hostname)

    Config_Product.load(hostname)
    Config_Coverage.load(hostname)
    Config_RateGroup.load(hostname)
    Config_AgeMapper.load(hostname)
    Config_ProductMapper.load(hostname)
    Config_RelationshipMapper.load(hostname)
    Config_ProductState.load(hostname)

    Config_ProductVariation.load(hostname)
    Config_ProductVariationState.load(hostname)

    Config_Benefit.load(hostname)
    Config_BenefitDuration.load(hostname)
    Config_BenefitState.load(hostname)

    Config_Provision.load(hostname)
    Config_ProvisionState.load(hostname)
    Config_ProvisionUI.load(hostname)
    Config_Factor.load(hostname)

    Config_BenefitProductVariation.load(hostname)
    Config_BenefitProvision.load(hostname)


def load_rate_table(hostname: str):  
    Config_RateTable.load(hostname)
    

def load_selection(hostname: str): 
    Selection_Plan.load(hostname)
    Selection_Benefit.load(hostname)
    Selection_BenefitDuration.load(hostname)
    Selection_Provision.load(hostname)
    Selection_AgeBand.load(hostname)