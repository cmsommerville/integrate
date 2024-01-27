from flask_restx import Namespace
from app.backend import resources as res

ns_crud = Namespace("crud", "Namespace containing standard CRUD endpoints")

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
    res.CRUD_ConfigAttributeDetail, "/attribute/detail/<int:id>", "/attribute/detail"
)
ns_crud.add_resource(res.CRUD_ConfigAttributeDetail_List, "/attribute/details")

ns_crud.add_resource(
    res.CRUD_ConfigAttributeSet,
    "/attribute/set/<string:config_attr_type_code>/<int:id>",
    "/attribute/set/<string:config_attr_type_code>",
)
ns_crud.add_resource(
    res.CRUD_ConfigAttributeSet_List, "/attribute/sets/<string:config_attr_type_code>"
)
ns_crud.add_resource(res.CRUD_ConfigProduct, "/product/<int:id>", "/product")
ns_crud.add_resource(res.CRUD_ConfigProduct_List, "/products")


ns_crud_product = Namespace("crud-product", "Namespace of product CRUD endpoints")

ns_crud_product.add_resource(res.CRUD_ConfigBenefit, "/benefit/<int:id>", "/benefit")
ns_crud_product.add_resource(res.CRUD_ConfigBenefit_List, "/benefits")
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitCovarianceSet_List, "/benefit-covariance/sets"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitProductVariation_List, "/benefit-variations"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigBenefitProvision_List, "/benefit-provisions"
)
ns_crud_product.add_resource(res.CRUD_ConfigBenefitState_List, "/benefit/states")
ns_crud_product.add_resource(res.CRUD_ConfigCoverage, "/coverage/<int:id>", "/coverage")
ns_crud_product.add_resource(res.CRUD_ConfigCoverage_List, "/coverages")
ns_crud_product.add_resource(res.CRUD_ConfigFactor_List, "/provision/factors")

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
    res.CRUD_ConfigProductVariationState_List, "/variation/states"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigProvision,
    "/provision/<string:provision_type>/<int:id>",
    "/provision/<string:provision_type>",
)
ns_crud_product.add_resource(
    res.CRUD_ConfigProvision_List, "/provisions/<string:provision_type>"
)
ns_crud_product.add_resource(res.CRUD_ConfigProvisionState_List, "/provision/states")
ns_crud_product.add_resource(
    res.CRUD_ConfigProvisionUI_List, "/provision/ui-components"
)
ns_crud_product.add_resource(
    res.CRUD_ConfigRateGroup, "/rate-group/<int:id>", "/rate-group"
)
ns_crud_product.add_resource(res.CRUD_ConfigRateGroup_List, "/rate-groups")
ns_crud_product.add_resource(
    res.CRUD_ConfigRateTable, "/rate-table/<int:id>", "/rate-table"
)
ns_crud_product.add_resource(res.CRUD_ConfigRateTable_List, "/rate-tables")


ns_crud_provision = Namespace("crud-provision", "Namespace of provision CRUD endpoints")

ns_crud_provision.add_resource(
    res.CRUD_ConfigProvisionState, "/state/<int:id>", "/state"
)
ns_crud_provision.add_resource(res.CRUD_ConfigProvisionUI, "/ui/<int:id>", "/ui")
ns_crud_provision.add_resource(res.CRUD_ConfigFactor, "/factor/<int:id>", "/factor")
ns_crud_provision.add_resource(
    res.CRUD_ConfigFactorRule,
    "/factor/<int:factor_id>/rule/<int:id>",
    "/factor/<int:factor_id>/rule",
)
ns_crud_provision.add_resource(
    res.CRUD_ConfigFactorRule_List, "/factor/<int:factor_id>/rules"
)


ns_crud_benefit = Namespace("crud-benefit", "Namespace of benefit CRUD endpoints")

ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitCovarianceDetail,
    "/covariance/detail/<int:id>",
    "/covariance/detail",
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitCovarianceDetail_List, "/covariance/details"
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitCovarianceSet, "/covariance/set/<int:id>", "/covariance/set"
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitDurationDetail,
    "/duration/detail/<int:id>",
    "/duration/detail",
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitDurationDetail_List, "/duration/details"
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitDurationSet, "/duration/set/<int:id>", "/duration/set"
)
ns_crud_benefit.add_resource(res.CRUD_ConfigBenefitDurationSet_List, "/duration/sets")
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitProductVariation, "/variation/<int:id>", "/variation"
)
ns_crud_benefit.add_resource(
    res.CRUD_ConfigBenefitProvision, "/provision/<int:id>", "/provision"
)
ns_crud_benefit.add_resource(res.CRUD_ConfigBenefitState, "/state/<int:id>", "/state")


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
    res.CRUD_RefRatingStrategy, "/rating-strategy/<int:id>", "/rating-strategy"
)
ns_ref.add_resource(res.CRUD_RefRatingStrategy_List, "/rating-strategies")
ns_ref.add_resource(res.CRUD_RefStates, "/state/<int:id>", "/state")
ns_ref.add_resource(res.CRUD_RefStates_List, "/states")
ns_ref.add_resource(res.CRUD_RefUnitCode, "/unit-type/<int:id>", "/unit-type")
ns_ref.add_resource(res.CRUD_RefUnitCode_List, "/unit-types")
