from flask_restx import Namespace
from app.backend import resources as res
from .util import add_routes

ns_base = Namespace("Base routes", "Namespace containing standard CRUD endpoints")
ns_product = Namespace("Product routes", "Namespace of product CRUD endpoints")
ns_benefit = Namespace("Benefit routes", "Namespace of benefit CRUD endpoints")
ns_benefit_duration = Namespace(
    "Benefit duration routes", "Namespace of benefit duration CRUD endpoints"
)
ns_coverage = Namespace("Coverage routes", "Namespace of coverage CRUD endpoints")
ns_plan_design = Namespace(
    "Plan design routes", "Namespace of plan design CRUD endpoints"
)
ns_provision = Namespace("Provision routes", "Namespace of provision CRUD endpoints")
ns_variation = Namespace(
    "Product variation routes", "Namespace of product variation CRUD endpoints"
)
ns_variation_state = Namespace(
    "Product variation state routes",
    "Namespace of product variation state CRUD endpoints",
)
ns_ref = Namespace(
    "Reference table routes", "Namespace of reference data CRUD endpoints"
)
ns_selection_base = Namespace(
    "Base selection routes", "Namespace containing standard selection endpoints"
)
ns_selection_benefit = Namespace(
    "Selection benefit routes",
    "Namespace containing standard benefit selection endpoints",
)
ns_selection_plan = Namespace(
    "Selection plan routes", "Namespace containing standard plan selection endpoints"
)

BASE_ROUTES = {
    "/age-band-sets/<int:set_id>/detail/<int:id>": res.CRUD_ConfigAgeBandDetail,
    "/age-band-sets/<int:set_id>/details": res.CRUD_ConfigAgeBandDetail_List,
    "/age-band-sets/<int:id>": res.CRUD_ConfigAgeBandSet,
    "/age-band-sets": res.CRUD_ConfigAgeBandSet_List,
    "/age-dist-set/<int:set_id>/detail/<int:id>": res.CRUD_ConfigAgeDistribution,
    "/age-dist-set/<int:set_id>/details": res.CRUD_ConfigAgeDistribution_List,
    "/age-dist-set/<int:id>": res.CRUD_ConfigAgeDistributionSet,
    "/age-dist-sets": res.CRUD_ConfigAgeDistributionSet_List,
    "/attrset/<int:set_id>/detail/<int:id>": res.CRUD_ConfigAttributeDetail,
    "/attrset/<int:set_id>/details": res.CRUD_ConfigAttributeDetail_List,
    "/attrset/<int:id>": res.CRUD_ConfigAttributeSet,
    "/attrsets": res.CRUD_ConfigAttributeSet_List,
    "/dropdown/<int:id>": res.CRUD_ConfigDropdownSet,
    "/dropdowns": res.CRUD_ConfigDropdownSet_List,
    "/mappers/<int:collection_id>/set/<int:id>": res.CRUD_ConfigRatingMapperSet,
    "/mappers/<int:collection_id>/sets": res.CRUD_ConfigRatingMapperSet_List,
    "/mappers/<int:id>": res.CRUD_ConfigRatingMapperCollection,
    "/mappers": res.CRUD_ConfigRatingMapperCollection_List,
    "/product/<int:id>": res.CRUD_ConfigProduct,
    "/products": res.CRUD_ConfigProduct_List,
}

PRODUCT_ROUTES = {
    "/benefit/<int:id>": res.CRUD_ConfigBenefit,
    "/benefits": res.CRUD_ConfigBenefit_List,
    "/cohorts": res.RateTableCohortsResource,
    "/coverage/<int:id>": res.CRUD_ConfigCoverage,
    "/coverages": res.CRUD_ConfigCoverage_List,
    "/plan-design/<int:id>": res.CRUD_ConfigPlanDesignSet_Product,
    "/plan-designs": res.CRUD_ConfigPlanDesignSet_Product_List,
    "/provision/<int:id>": res.CRUD_ConfigProvision,
    "/provisions": res.CRUD_ConfigProvision_List,
    "/rate-group/<int:id>": res.CRUD_ConfigRateGroup,
    "/rate-groups": res.CRUD_ConfigRateGroup_List,
    "/state/<int:id>": res.CRUD_ConfigProductState,
    "/states": res.CRUD_ConfigProductState_List,
    "/variation/<int:id>": res.CRUD_ConfigProductVariation,
    "/variations": res.CRUD_ConfigProductVariation_List,
}

BENEFIT_ROUTES = {
    "/provision/<int:id>": res.CRUD_ConfigBenefitProvision,
    "/provisions": res.CRUD_ConfigBenefitProvision_List,
    "/duration/<int:id>": res.CRUD_ConfigBenefitDurationSet,
    "/durations": res.CRUD_ConfigBenefitDurationSet_List,
    "/state/<int:id>": res.CRUD_ConfigBenefitVariationState,
    "/states": res.CRUD_ConfigBenefitVariationState_List,
    "/states:update-rateset": res.ConfigBenefitVariationStateRateset,
    "/rateset/<int:id>": res.CRUD_ConfigRateTableSet,
    "/ratesets": res.CRUD_ConfigRateTableSet_List,
}

BENEFIT_DURATION_ROUTES = {
    "/detail/<int:id>": res.CRUD_ConfigBenefitDurationDetail,
    "/details": res.CRUD_ConfigBenefitDurationDetail_List,
}

COVERAGE_ROUTES = {
    "/plan-design/<int:id>": res.CRUD_ConfigPlanDesignSet_Coverage,
    "/plan-designs": res.CRUD_ConfigPlanDesignSet_Coverage_List,
}

PLAN_DESIGN_ROUTES = {
    "/benefit/<int:id>": res.CRUD_ConfigPlanDesignDetail_Benefit,
    "/benefits": res.CRUD_ConfigPlanDesignDetail_Benefit_List,
    "/pd/<int:id>": res.CRUD_ConfigPlanDesignDetail_PlanDesign,
    "/pds": res.CRUD_ConfigPlanDesignDetail_PlanDesign_List,
}

PROVISION_ROUTES = {
    "/benefit/<int:id>": res.CRUD_ConfigBenefitProvision,
    "/benefits": res.CRUD_ConfigBenefitProvision_List,
    "/state/<int:id>": res.CRUD_ConfigProvisionState,
    "/states": res.CRUD_ConfigProvisionState_List,
    "/factor/<int:id>": res.CRUD_ConfigFactorSet,
    "/factors": res.CRUD_ConfigFactorSet_List,
    "/factor/<int:factor_id>/rule/<int:id>": res.CRUD_ConfigFactorRule,
    "/factor/<int:factor_id>/rules": res.CRUD_ConfigFactorRule_List,
    "/provision/ui-components": res.CRUD_ConfigProvisionUI_List,
}

PRODUCT_VARIATION_ROUTES = {
    "/state/<int:id>": res.CRUD_ConfigProductVariationState,
    "/states": res.CRUD_ConfigProductVariationState_List,
    "/plan-designs:states": res.Resource_ConfigProductVariation_SetPlanDesignVariationStates,
}

PRODUCT_VARIATION_STATE_ROUTES = {
    "/plan-design/<int:id>": res.CRUD_ConfigPlanDesignVariationState,
    "/plan-designs": res.CRUD_ConfigPlanDesignVariationState_List,
    ":cvgpd": res.Resource_ConfigPlanDesignVariationState_CoveragePlanDesignList,
    ":prdpd": res.Resource_ConfigPlanDesignVariationState_ProductPlanDesignList,
}

REF_ROUTES = {
    "/attr-mapper-type/<int:id>": res.CRUD_RefAttrMapperType,
    "/attr-mapper-types": res.CRUD_RefAttrMapperType_List,
    "/benefit/<int:id>": res.CRUD_RefBenefit,
    "/benefits": res.CRUD_RefBenefit_List,
    "/census-strategy/<int:id>": res.CRUD_RefCensusStrategy,
    "/census-strategies": res.CRUD_RefCensusStrategy_List,
    "/comparison-operator/<int:id>": res.CRUD_RefComparisonOperator,
    "/comparison-operators": res.CRUD_RefComparisonOperator_List,
    "/component-type/<int:id>": res.CRUD_RefComponentTypes,
    "/component-types": res.CRUD_RefComponentTypes_List,
    "/data-type/<int:id>": res.CRUD_RefDataTypes,
    "/data-types": res.CRUD_RefDataTypes_List,
    "/factor-type/<int:id>": res.CRUD_RefFactorType,
    "/factor-types": res.CRUD_RefFactorType_List,
    "/input-type/<int:id>": res.CRUD_RefInputTypes,
    "/input-types": res.CRUD_RefInputTypes_List,
    "/optionality/<int:id>": res.CRUD_RefOptionality,
    "/optionalities": res.CRUD_RefOptionality_List,
    "/plan-status/<int:id>": res.CRUD_RefOptionality,
    "/plan-statuses": res.CRUD_RefOptionality_List,
    "/premium-frequency/<int:id>": res.CRUD_RefPremiumFrequency,
    "/premium-frequencies": res.CRUD_RefPremiumFrequency_List,
    "/product-variation/<int:id>": res.CRUD_RefProductVariation,
    "/product-variations": res.CRUD_RefProductVariation_List,
    "/provision/<int:id>": res.CRUD_RefProvision,
    "/provisions": res.CRUD_RefProvision_List,
    "/rate-frequency/<int:id>": res.CRUD_RefRateFrequency,
    "/rate-frequencies": res.CRUD_RefRateFrequency_List,
    "/rating-strategy/<int:id>": res.CRUD_RefRatingStrategy,
    "/rating-strategies": res.CRUD_RefRatingStrategy_List,
    "/state/<int:id>": res.CRUD_RefStates,
    "/states": res.CRUD_RefStates_List,
    "/unit-type/<int:id>": res.CRUD_RefUnitCode,
    "/unit-types": res.CRUD_RefUnitCode_List,
}

SELECTION_BASE_ROUTES = {
    "/plan/<int:id>": res.CRUD_SelectionPlan,
    "/plan": res.CRUD_SelectionPlan_CreateOnly,
}

SELECTION_PLAN_ROUTES = {
    "/benefit/<int:id>": res.CRUD_SelectionBenefit,
    "/benefits": res.CRUD_SelectionBenefit_List,
    "/provision/<int:id>": res.CRUD_SelectionProvision,
    "/provision": res.CRUD_SelectionProvision_CreateOnly,
    "/provisions": res.CRUD_SelectionProvision_List,
    "/age-band/<int:id>": res.CRUD_SelectionAgeBand,
    "/age-bands": res.CRUD_SelectionAgeBand_List,
    "/mapper-set/<int:id>": res.CRUD_SelectionRatingMapperSet,
    "/mapper-sets": res.CRUD_SelectionRatingMapperSet_List,
}

SELECTION_BENEFIT_ROUTES = {
    "/duration/<int:id>": res.CRUD_SelectionBenefitDuration,
    "/durations": res.CRUD_SelectionBenefitDuration_List,
}


add_routes(ns_base, BASE_ROUTES)
add_routes(ns_product, PRODUCT_ROUTES)
add_routes(ns_benefit, BENEFIT_ROUTES)
add_routes(ns_benefit_duration, BENEFIT_DURATION_ROUTES)
add_routes(ns_coverage, COVERAGE_ROUTES)
add_routes(ns_plan_design, PLAN_DESIGN_ROUTES)
add_routes(ns_provision, PROVISION_ROUTES)
add_routes(ns_variation, PRODUCT_VARIATION_ROUTES)
add_routes(ns_variation_state, PRODUCT_VARIATION_STATE_ROUTES)
add_routes(ns_ref, REF_ROUTES)
add_routes(ns_selection_base, SELECTION_BASE_ROUTES)
add_routes(ns_selection_plan, SELECTION_PLAN_ROUTES)
add_routes(ns_selection_benefit, SELECTION_BENEFIT_ROUTES)
