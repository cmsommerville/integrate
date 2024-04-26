from . import (
    Config_AgeBand,
    Config_AgeDistribution,
    Config_AttributeSet,
    Config_Benefit,
    Config_BenefitDuration,
    Config_BenefitProvision,
    Config_BenefitVariationState,
    Config_Coverage,
    Config_Dropdown,
    Config_Factor,
    Config_PlanDesign_Coverage,
    Config_PlanDesign_Product,
    Config_PlanDesignVariationState,
    Config_Product,
    Config_ProductState,
    Config_ProductVariation,
    Config_ProductVariationState,
    Config_Provision,
    Config_ProvisionState,
    Config_RateGroup,
    Config_RateTable,
    Config_RatingMapper,
    Ref_AttrMapperType,
    Ref_Benefit,
    Ref_CensusStrategy,
    Ref_ComparisonOperator,
    Ref_DataTypes,
    Ref_InputType,
    Ref_Optionality,
    Ref_PlanStatus,
    Ref_PremiumFrequency,
    Ref_ProductVariation,
    Ref_Provision,
    Ref_RateFrequency,
    Ref_RatingStrategy,
    Ref_States,
    Ref_UnitType,
    Selection_AgeBand,
    Selection_Benefit,
    Selection_BenefitDuration,
    Selection_Plan,
    Selection_Provision,
    Selection_RatingMappers,
    Random_Selection,
    Selection_RPC,
    Auth_RolesPermissions,
    Auth_Superuser,
)


def load_roles_permissions(hostname: str, *args, **kwargs):
    try:
        Auth_RolesPermissions.load(hostname, **kwargs)
    except Exception:
        pass


def load_refdata(hostname: str, *args, **kwargs):
    res = Auth_Superuser.login(hostname, **kwargs)
    headers = res.headers
    kwargs["headers"] = headers

    Ref_AttrMapperType.load(hostname, **kwargs)
    Ref_Benefit.load(hostname, **kwargs)
    Ref_CensusStrategy.load(hostname, **kwargs)
    Ref_ComparisonOperator.load(hostname, **kwargs)
    Ref_DataTypes.load(hostname, **kwargs)
    Ref_InputType.load(hostname, **kwargs)
    Ref_Optionality.load(hostname, **kwargs)
    Ref_PlanStatus.load(hostname, **kwargs)
    Ref_PremiumFrequency.load(hostname, **kwargs)
    Ref_ProductVariation.load(hostname, **kwargs)
    Ref_Provision.load(hostname, **kwargs)
    Ref_RateFrequency.load(hostname, **kwargs)
    Ref_RatingStrategy.load(hostname, **kwargs)
    Ref_States.load(hostname, **kwargs)
    Ref_UnitType.load(hostname, **kwargs)


def load_config(hostname: str, *args, **kwargs):
    Config_Dropdown.load(hostname, **kwargs)
    Config_AgeBand.load(hostname, **kwargs)
    Config_AttributeSet.load(hostname, **kwargs)
    Config_RatingMapper.load(hostname, **kwargs)
    Config_AgeDistribution.load(hostname, **kwargs)
    Config_Product.load(hostname, **kwargs)
    Config_ProductState.load(hostname, **kwargs)
    Config_ProductVariation.load(hostname, **kwargs)
    Config_ProductVariationState.load(hostname, **kwargs)
    Config_RateGroup.load(hostname, **kwargs)
    Config_Coverage.load(hostname, **kwargs)
    Config_Benefit.load(hostname, **kwargs)
    Config_BenefitDuration.load(hostname, **kwargs)
    Config_Provision.load(hostname, **kwargs)
    Config_ProvisionState.load(hostname, **kwargs)
    Config_Factor.load(hostname, **kwargs)
    Config_BenefitVariationState.load(hostname, **kwargs)
    Config_RateTable.load(hostname, **kwargs)
    Config_BenefitProvision.load(hostname, **kwargs)
    Config_PlanDesign_Coverage.load(hostname, **kwargs)
    Config_PlanDesign_Product.load(hostname, **kwargs)
    Config_PlanDesignVariationState.load(hostname, **kwargs)


def load_generic(hostname, *args, **kwargs):
    instance = Selection_RPC.TestSelectionRPC_CreateDefaultPlan()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_Plan()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_Benefit()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_BenefitDuration()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_Provision()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_RatingMapper()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_AgeBands()
    instance.execute()
    instance.rollback()

    instance = Selection_RPC.TestSelectionRPC_ProductVariation()
    instance.execute()
    instance.rollback()


def load_selection(hostname, *args, **kwargs):
    Selection_Plan.load(hostname, **kwargs)
    Selection_RatingMappers.load(hostname, **kwargs)
    Selection_Benefit.load(hostname, **kwargs)
    Selection_BenefitDuration.load(hostname, **kwargs)
    Selection_Provision.load(hostname, **kwargs)
    Selection_AgeBand.load(hostname, **kwargs)


def create_random_plan(hostname, product_code, *args, **kwargs):
    return Random_Selection.load(hostname, product_code, **kwargs)
