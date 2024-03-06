from flask_restx import Namespace
from app.backend import resources as res

ns_crud = Namespace("crud", "Namespace containing standard CRUD endpoints")
ns_selection = Namespace(
    "selection", "Namespace containing standard selection endpoints"
)

ns_crud.add_resource(
    res.CRUD_ConfigAgeBandDetail, "/age-band/detail/<int:id>", "/age-band/detail"
)
ns_crud.add_resource(res.CRUD_ConfigAgeBandDetail_List, "/age-band/details")
ns_crud.add_resource(
    res.CRUD_ConfigAgeBandSet, "/age-band/set/<int:id>", "/age-band/set"
)
ns_crud.add_resource(res.CRUD_ConfigAgeBandSet_List, "/age-band/sets")
ns_crud.add_resource(
    res.CRUD_ConfigAgeDistribution,
    "/age-distribution/detail/<int:id>",
    "/age-distribution/detail",
)
ns_crud.add_resource(res.CRUD_ConfigAgeDistribution_List, "/age-distribution/details")
ns_crud.add_resource(
    res.CRUD_ConfigAgeDistributionSet,
    "/age-distribution/set/<int:id>",
    "/age-distribution/set",
)
ns_crud.add_resource(res.CRUD_ConfigAgeDistributionSet_List, "/age-distribution/sets")
ns_crud.add_resource(
    res.CRUD_ConfigAttributeSet,
    "/attribute/set/<int:id>",
    "/attribute/set",
)
ns_crud.add_resource(res.CRUD_ConfigAttributeSet_List, "/attribute/sets")


ns_crud.add_resource(
    res.CRUD_ConfigAttributeDetail,
    "/attribute/set/<int:set_id>/detail/<int:id>",
    "/attribute/set/<int:set_id>/detail",
)
ns_crud.add_resource(
    res.CRUD_ConfigAttributeDetail_List, "/attribute/set/<int:set_id>/details"
)

ns_crud.add_resource(
    res.CRUD_ConfigDropdownSet,
    "/dropdown/set/<int:id>",
    "/dropdown/set",
)
ns_crud.add_resource(res.CRUD_ConfigDropdownSet_List, "/dropdown/sets")


ns_crud.add_resource(res.CRUD_ConfigProduct, "/product/<int:id>", "/product")
ns_crud.add_resource(res.CRUD_ConfigProduct_List, "/products")
ns_crud.add_resource(
    res.CRUD_ConfigRatingMapperCollection,
    "/mappers/collection/<int:id>",
    "/mappers/collection",
)
ns_crud.add_resource(res.CRUD_ConfigRatingMapperCollection_List, "/mappers/collections")

ns_crud.add_resource(
    res.CRUD_ConfigRatingMapperSet,
    "/mappers/collection/<int:collection_id>/set/<int:id>",
    "/mappers/collection/<int:collection_id>/set",
)
ns_crud.add_resource(
    res.CRUD_ConfigRatingMapperSet_List, "/mappers/collection/<int:collection_id>/sets"
)

ns_crud_product = Namespace("crud-product", "Namespace of product CRUD endpoints")

ns_crud_product.add_resource(res.CRUD_ConfigBenefit, "/benefit/<int:id>", "/benefit")
ns_crud_product.add_resource(res.CRUD_ConfigBenefit_List, "/benefits")
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitProvision,
    "/benefit/<int:benefit_id>/provision/<int:id>",
    "/benefit/<int:benefit_id>/provision",
    "/provision/<int:provision_id>/benefit/<int:id>",
    "/provision/<int:provision_id>/benefit",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitProvision_List,
    "/benefit/<int:benefit_id>/provisions",
    "/provision/<int:provision_id>/benefits",
)
ns_crud_product.add_resource(res.CRUD_ConfigCoverage, "/coverage/<int:id>", "/coverage")
ns_crud_product.add_resource(res.CRUD_ConfigCoverage_List, "/coverages")

ns_crud_product.add_resource(res.CRUD_ConfigProductState, "/state/<int:id>", "/state")
ns_crud_product.add_resource(res.CRUD_ConfigProductState_List, "/states")
ns_crud_product.add_resource(
    res.CRUD_ConfigProductVariation, "/variation/<int:id>", "/variation"
)
ns_crud_product.add_resource(res.CRUD_ConfigProductVariation_List, "/variations")
ns_crud_product.add_resource(
    res.CRUD_ConfigProductVariationState,
    "/variation/<int:product_variation_id>/state/<int:id>",
    "/variation/<int:product_variation_id>/state",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigProductVariationState_List,
    "/variation/<int:product_variation_id>/states",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigProvision,
    "/provision/<int:id>",
    "/provision",
)
ns_crud_product.add_resource(res.CRUD_ConfigProvision_List, "/provisions")

ns_crud_product.add_resource(
    res.CRUD_ConfigProvisionState,
    "/provision/<int:provision_id>/state/<int:id>",
    "/provision/<int:provision_id>/state",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigProvisionState_List, "/provision/<int:provision_id>/states"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigFactorSet,
    "/provision/<int:provision_id>/factor/<int:id>",
    "/provision/<int:provision_id>/factor",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigFactorSet_List,
    "/provision/<int:provision_id>/factors",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigFactorRule,
    "/provision/<int:provision_id>/factor/<int:factor_id>/rule/<int:id>",
    "/provision/<int:provision_id>/factor/<int:factor_id>/rule",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigFactorRule_List,
    "/provision/<int:provision_id>/factor/<int:factor_id>/rules",
)
ns_crud_product.add_resource(
    res.RateTableCohortsResource,
    "/cohorts",
)


ns_crud_product.add_resource(
    res.CRUD_ConfigProvisionUI_List, "/provision/ui-components"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigRateGroup, "/rate-group/<int:id>", "/rate-group"
)
ns_crud_product.add_resource(res.CRUD_ConfigRateGroup_List, "/rate-groups")

ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitDurationDetail,
    "/benefit/<int:benefit_id>/duration-set/<int:set_id>/detail/<int:id>",
    "/benefit/<int:benefit_id>/duration-set/<int:set_id>/detail",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitDurationDetail_List,
    "/benefit/<int:benefit_id>/duration-set/<int:set_id>/details",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitDurationSet,
    "/benefit/<int:benefit_id>/duration-set/<int:id>",
    "/benefit/<int:benefit_id>/duration-set",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitDurationSet_List, "/benefit/<int:benefit_id>/duration-sets"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitVariationState,
    "/benefit/<int:benefit_id>/state/<int:id>",
    "/benefit/<int:benefit_id>/state",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitVariationState_List,
    "/benefit/<int:benefit_id>/states",
)

ns_crud_product.add_resource(
    res.ConfigBenefitVariationStateRateset,
    "/benefit/<int:benefit_id>/states:update-rateset",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigRateTableSet,
    "/benefit/<int:benefit_id>/rateset/<int:id>",
    "/benefit/<int:benefit_id>/rateset",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigRateTableSet_List, "/benefit/<int:benefit_id>/rateset"
)


ns_crud_provision = Namespace("crud-provision", "Namespace of provision CRUD endpoints")

ns_crud_provision.add_resource(res.CRUD_ConfigProvisionUI, "/ui/<int:id>", "/ui")


ns_crud_benefit = Namespace("crud-benefit", "Namespace of benefit CRUD endpoints")

ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitProvision, "/provision/<int:id>", "/provision"
)
ns_ref = Namespace("crud-ref", "Namespace of reference data CRUD endpoints")


ns_ref.add_resource(
    res.CRUD_RefAttrMapperType, "/attr-mapper-type/<int:id>", "/attr-mapper-type"
)
ns_ref.add_resource(res.CRUD_RefAttrMapperType_List, "/attr-mapper-types")
ns_ref.add_resource(res.CRUD_RefBenefit, "/benefit/<int:id>", "/benefit")
ns_ref.add_resource(res.CRUD_RefBenefit_List, "/benefits")
ns_ref.add_resource(
    res.CRUD_RefCensusStrategy, "/census-strategy/<int:id>", "/census-strategy"
)
ns_ref.add_resource(res.CRUD_RefCensusStrategy_List, "/census-strategies")
ns_ref.add_resource(
    res.CRUD_RefComparisonOperator,
    "/comparison-operator/<int:id>",
    "/comparison-operator",
)
ns_ref.add_resource(res.CRUD_RefComparisonOperator_List, "/comparison-operators")
ns_ref.add_resource(
    res.CRUD_RefComponentTypes, "/component-type/<int:id>", "/component-type"
)
ns_ref.add_resource(res.CRUD_RefComponentTypes_List, "/component-types")
ns_ref.add_resource(res.CRUD_RefDataTypes, "/data-type/<int:id>", "/data-type")
ns_ref.add_resource(res.CRUD_RefDataTypes_List, "/data-types")
ns_ref.add_resource(res.CRUD_RefFactorType, "/factor-type/<int:id>", "/factor-type")
ns_ref.add_resource(res.CRUD_RefFactorType_List, "/factor-types")
ns_ref.add_resource(res.CRUD_RefInputTypes, "/input-type/<int:id>", "/input-type")
ns_ref.add_resource(res.CRUD_RefInputTypes_List, "/input-types")
ns_ref.add_resource(res.CRUD_RefOptionality, "/optionality/<int:id>", "/optionality")
ns_ref.add_resource(res.CRUD_RefOptionality_List, "/optionalities")
ns_ref.add_resource(res.CRUD_RefOptionality, "/plan-status/<int:id>", "/plan-status")
ns_ref.add_resource(res.CRUD_RefOptionality_List, "/plan-statuses")
ns_ref.add_resource(
    res.CRUD_RefPremiumFrequency, "/premium-frequency/<int:id>", "/premium-frequency"
)
ns_ref.add_resource(res.CRUD_RefPremiumFrequency_List, "/premium-frequencies")
ns_ref.add_resource(
    res.CRUD_RefProductVariation, "/product-variation/<int:id>", "/product-variation"
)
ns_ref.add_resource(res.CRUD_RefProductVariation_List, "/product-variations")
ns_ref.add_resource(res.CRUD_RefProvision, "/provision/<int:id>", "/provision")
ns_ref.add_resource(res.CRUD_RefProvision_List, "/provisions")
ns_ref.add_resource(
    res.CRUD_RefRateFrequency, "/rate-frequency/<int:id>", "/rate-frequency"
)
ns_ref.add_resource(res.CRUD_RefRateFrequency_List, "/rate-frequencies")
ns_ref.add_resource(
    res.CRUD_RefRatingStrategy, "/rating-strategy/<int:id>", "/rating-strategy"
)
ns_ref.add_resource(res.CRUD_RefRatingStrategy_List, "/rating-strategies")
ns_ref.add_resource(res.CRUD_RefStates, "/state/<int:id>", "/state")
ns_ref.add_resource(res.CRUD_RefStates_List, "/states")
ns_ref.add_resource(res.CRUD_RefUnitCode, "/unit-type/<int:id>", "/unit-type")
ns_ref.add_resource(res.CRUD_RefUnitCode_List, "/unit-types")


ns_selection.add_resource(res.CRUD_SelectionPlan, "/plan/<int:id>", "/plan")
ns_selection.add_resource(res.CRUD_SelectionPlan_List, "/plans")
ns_selection.add_resource(
    res.CRUD_SelectionBenefit,
    "/plan/<int:plan_id>/benefit/<int:id>",
    "/plan/<int:plan_id>/benefit",
)
ns_selection.add_resource(
    res.CRUD_SelectionBenefit_List,
    "/plan/<int:plan_id>/benefits",
)
ns_selection.add_resource(
    res.CRUD_SelectionProvision,
    "/plan/<int:plan_id>/provision/<int:id>",
    "/plan/<int:plan_id>/provision",
)
ns_selection.add_resource(
    res.CRUD_SelectionProvision_List,
    "/plan/<int:plan_id>/provisions",
)

ns_selection.add_resource(
    res.CRUD_SelectionBenefitDuration,
    "/plan/<int:plan_id>/benefit/<int:benefit_id>/duration/<int:id>",
    "/plan/<int:plan_id>/benefit/<int:benefit_id>/duration",
)
ns_selection.add_resource(
    res.CRUD_SelectionBenefitDuration_List,
    "/plan/<int:plan_id>/benefit/<int:benefit_id>/durations",
)

ns_selection.add_resource(
    res.CRUD_SelectionAgeBand,
    "/plan/<int:plan_id>/age-band/<int:id>",
    "/plan/<int:plan_id>/age-band",
)
ns_selection.add_resource(
    res.CRUD_SelectionAgeBand_List,
    "/plan/<int:plan_id>/age-bands",
)

ns_selection.add_resource(
    res.CRUD_SelectionRatingMapperSet,
    "/plan/<int:plan_id>/mapper-set/<int:id>",
    "/plan/<int:plan_id>/mapper-set",
)
ns_selection.add_resource(
    res.CRUD_SelectionRatingMapperSet_List,
    "/plan/<int:plan_id>/mapper-sets",
)
