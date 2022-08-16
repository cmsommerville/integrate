from flask_restx import Namespace

from .Config_AgeBandDetail import CRUD_ConfigAgeBandDetail, CRUD_ConfigAgeBandDetail_List
from .Config_AgeBandSet import CRUD_ConfigAgeBandSet, CRUD_ConfigAgeBandSet_List
from .Config_AgeDistribution import CRUD_ConfigAgeDistribution, CRUD_ConfigAgeDistribution_List
from .Config_AgeDistributionSet import CRUD_ConfigAgeDistributionSet, CRUD_ConfigAgeDistributionSet_List
from .Config_AgeMapperDetail import  CRUD_ConfigAgeMapperDetail, CRUD_ConfigAgeMapperDetail_List
from .Config_AttributeDetail import CRUD_ConfigAttributeDetail, CRUD_ConfigAttributeDetail_List
from .Config_AttributeDistribution import CRUD_ConfigAttributeDistribution, CRUD_ConfigAttributeDistribution_List
from .Config_AttributeDistributionSet import CRUD_ConfigAttributeDistributionSet_Gender, CRUD_ConfigAttributeDistributionSet_Gender_List, CRUD_ConfigAttributeDistributionSet_SmokerStatus, CRUD_ConfigAttributeDistributionSet_SmokerStatus_List
from .Config_AttributeSet import CRUD_ConfigAttributeSet_Gender, CRUD_ConfigAttributeSet_SmokerStatus, CRUD_ConfigAttributeSet_Relationship,  \
    CRUD_ConfigAttributeSet_Gender_List, CRUD_ConfigAttributeSet_SmokerStatus_List, CRUD_ConfigAttributeSet_Relationship_List
from .Config_Benefit import CRUD_ConfigBenefit, CRUD_ConfigBenefit_List
from .Config_BenefitDurationDetail import CRUD_ConfigBenefitDurationDetail, CRUD_ConfigBenefitDurationDetail_List
from .Config_BenefitDurationSet import CRUD_ConfigBenefitDurationSet, CRUD_ConfigBenefitDurationSet_List
from .Config_BenefitProductVariation import CRUD_ConfigBenefitProductVariation, CRUD_ConfigBenefitProductVariation_List
from .Config_BenefitProvision import CRUD_ConfigBenefitProvision, CRUD_ConfigBenefitProvision_List
from .Config_BenefitState import CRUD_ConfigBenefitState, CRUD_ConfigBenefitState_List
from .Config_Coverage import CRUD_ConfigCoverage, CRUD_ConfigCoverage_List 
from .Config_Factor import CRUD_ConfigFactor, CRUD_ConfigFactor_List
from .Config_FactorRule import CRUD_ConfigFactorRule, CRUD_ConfigFactorRule_List
from .Config_Product import CRUD_ConfigProduct, CRUD_ConfigProduct_List 
from .Config_ProductMapperDetail import CRUD_ConfigProductMapperDetail, CRUD_ConfigProductMapperDetail_List
from .Config_ProductMapperSet import CRUD_ConfigProductMapperSet_Gender, CRUD_ConfigProductMapperSet_Gender_List, CRUD_ConfigProductMapperSet_SmokerStatus, CRUD_ConfigProductMapperSet_SmokerStatus_List
from .Config_ProductState import CRUD_ConfigProductState, CRUD_ConfigProductState_List
from .Config_ProductVariation import CRUD_ConfigProductVariation, CRUD_ConfigProductVariation_List
from .Config_ProductVariationState import CRUD_ConfigProductVariationState, CRUD_ConfigProductVariationState_List
from .Config_Provision import CRUD_ConfigProvision_Product, CRUD_ConfigProvision_Product_List,CRUD_ConfigProvision_RateTable, CRUD_ConfigProvision_RateTable_List
from .Config_ProvisionState import CRUD_ConfigProvisionState, CRUD_ConfigProvisionState_List
from .Config_ProvisionUI import CRUD_ConfigProvisionUI, CRUD_ConfigProvisionUI_List
from .Config_RateGroup import CRUD_ConfigRateGroup, CRUD_ConfigRateGroup_List
from .Config_RateTable import CRUD_ConfigRateTable, CRUD_ConfigRateTable_List
from .Config_RelationshipMapperDetail import CRUD_ConfigRelationshipMapperDetail, CRUD_ConfigRelationshipMapperDetail_List
from .Config_RelationshipMapperSet import CRUD_ConfigRelationshipMapperSet, CRUD_ConfigRelationshipMapperSet_List
from .Ref_Master import *
from .Ref_States import CRUD_RefStates, CRUD_RefStates_List

from .Selection_AgeBand import CRUD_SelectionAgeBand, CRUD_SelectionAgeBand_List
from .Selection_Benefit import CRUD_SelectionBenefit, CRUD_SelectionBenefit_List
from .Selection_BenefitDuration import CRUD_SelectionBenefitDuration, CRUD_SelectionBenefitDuration_List
from .Selection_CensusDetail import CRUD_SelectionCensusDetail, CRUD_SelectionCensusDetail_List
from .Selection_CensusSet import CRUD_SelectionCensusSet, CRUD_SelectionCensusSet_List
from .Selection_Plan import CRUD_SelectionPlan, CRUD_SelectionPlan_List
from .Selection_Provision import CRUD_SelectionProvision, CRUD_SelectionProvision_List

ns_crud = Namespace("crud", "Namespace containing standard CRUD endpoints")

ns_crud.add_resource(CRUD_ConfigAgeBandDetail, '/crud/config/age-band-detail/<int:id>', '/crud/config/age-band-detail')
ns_crud.add_resource(CRUD_ConfigAgeBandDetail_List, '/crud/config/age-band-detail-list')
ns_crud.add_resource(CRUD_ConfigAgeBandSet, '/crud/config/age-band-set/<int:id>', '/crud/config/age-band-set')
ns_crud.add_resource(CRUD_ConfigAgeBandSet_List, '/crud/config/age-band-set-list')
ns_crud.add_resource(CRUD_ConfigAgeDistribution, '/crud/config/age-distribution/<int:id>', '/crud/config/age-distribution')
ns_crud.add_resource(CRUD_ConfigAgeDistribution_List, '/crud/config/age-distribution-list')
ns_crud.add_resource(CRUD_ConfigAgeDistributionSet, '/crud/config/age-distribution-set/<int:id>', '/crud/config/age-distribution-set')
ns_crud.add_resource(CRUD_ConfigAgeDistributionSet_List, '/crud/config/age-distribution-set-list')
ns_crud.add_resource(CRUD_ConfigAgeMapperDetail, '/crud/config/age-mapper-detail/<int:id>', '/crud/config/age-mapper-detail')
ns_crud.add_resource(CRUD_ConfigAgeMapperDetail_List, '/crud/config/age-mapper-detail-list')
ns_crud.add_resource(CRUD_ConfigAttributeDetail, '/crud/config/attribute-detail/<int:id>', '/crud/config/attribute-detail')
ns_crud.add_resource(CRUD_ConfigAttributeDetail_List, '/crud/config/attribute-detail-list')
ns_crud.add_resource(CRUD_ConfigAttributeDistribution, '/crud/config/attribute-distribution/<int:id>', '/crud/config/attribute-distribution')
ns_crud.add_resource(CRUD_ConfigAttributeDistribution_List, '/crud/config/attribute-distribution-list')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_Gender, '/crud/config/attribute-distribution-set-gender/<int:id>', '/crud/config/attribute-distribution-set-gender')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_Gender_List, '/crud/config/attribute-distribution-set-gender-list')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_SmokerStatus, '/crud/config/attribute-distribution-set-smoker-status/<int:id>', '/crud/config/attribute-distribution-set-smoker-status')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_SmokerStatus_List, '/crud/config/attribute-distribution-set-smoker-status-list')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Gender, '/crud/config/attribute-set-gender/<int:id>', '/crud/config/attribute-set-gender')
ns_crud.add_resource(CRUD_ConfigAttributeSet_SmokerStatus, '/crud/config/attribute-set-smoker-status/<int:id>', '/crud/config/attribute-set-smoker-status')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Relationship, '/crud/config/attribute-set-relationship/<int:id>', '/crud/config/attribute-set-relationship')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Gender_List, '/crud/config/attribute-set-gender-list')
ns_crud.add_resource(CRUD_ConfigAttributeSet_SmokerStatus_List, '/crud/config/attribute-set-smoker-status-list')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Relationship_List, '/crud/config/attribute-set-relationship-list')
ns_crud.add_resource(CRUD_ConfigBenefit, '/crud/config/benefit/<int:id>', '/crud/config/benefit')
ns_crud.add_resource(CRUD_ConfigBenefit_List, '/crud/config/benefit-list')
ns_crud.add_resource(CRUD_ConfigBenefitDurationDetail, '/crud/config/benefit-duration-detail/<int:id>', '/crud/config/benefit-duration-detail')
ns_crud.add_resource(CRUD_ConfigBenefitDurationDetail_List, '/crud/config/benefit-duration-detail-list')
ns_crud.add_resource(CRUD_ConfigBenefitDurationSet, '/crud/config/benefit-duration-set/<int:id>', '/crud/config/benefit-duration-set')
ns_crud.add_resource(CRUD_ConfigBenefitDurationSet_List, '/crud/config/benefit-duration-set-list')
ns_crud.add_resource(CRUD_ConfigBenefitProductVariation, '/crud/config/benefit-product-variation/<int:id>', '/crud/config/benefit-product-variation')
ns_crud.add_resource(CRUD_ConfigBenefitProductVariation_List, '/crud/config/benefit-product-variation-list')
ns_crud.add_resource(CRUD_ConfigBenefitProvision, '/crud/config/benefit-provision/<int:id>', '/crud/config/benefit-provision')
ns_crud.add_resource(CRUD_ConfigBenefitProvision_List, '/crud/config/benefit-provision-list')
ns_crud.add_resource(CRUD_ConfigBenefitState, '/crud/config/benefit-state/<int:id>', '/crud/config/benefit-state')
ns_crud.add_resource(CRUD_ConfigBenefitState_List, '/crud/config/benefit-state-list')
ns_crud.add_resource(CRUD_ConfigCoverage, '/crud/config/coverage/<int:id>', '/crud/config/coverage')
ns_crud.add_resource(CRUD_ConfigCoverage_List, '/crud/config/coverage-list')
ns_crud.add_resource(CRUD_ConfigFactor, '/crud/config/factor/<int:id>', '/crud/config/factor')
ns_crud.add_resource(CRUD_ConfigFactor_List, '/crud/config/factor-list')
ns_crud.add_resource(CRUD_ConfigFactorRule, '/crud/config/factor-rule/<int:id>', '/crud/config/factor-rule')
ns_crud.add_resource(CRUD_ConfigFactorRule_List, '/crud/config/factor-rule-list')
ns_crud.add_resource(CRUD_ConfigProduct, '/crud/config/product/<int:id>', '/crud/config/product')
ns_crud.add_resource(CRUD_ConfigProduct_List, '/crud/config/product-list')
ns_crud.add_resource(CRUD_ConfigProductMapperDetail, '/crud/config/product-mapper-detail/<int:id>', '/crud/config/product-mapper-detail')
ns_crud.add_resource(CRUD_ConfigProductMapperDetail_List, '/crud/config/product-mapper-detail-list')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_Gender, '/crud/config/product-mapper-set-gender/<int:id>', '/crud/config/product-mapper-set-gender')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_Gender_List, '/crud/config/product-mapper-set-gender-list')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_SmokerStatus, '/crud/config/product-mapper-set-smoker-status/<int:id>', '/crud/config/product-mapper-set-smoker-status')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_SmokerStatus_List, '/crud/config/product-mapper-set-smoker-status-list')
ns_crud.add_resource(CRUD_ConfigProductState, '/crud/config/product-state/<int:id>', '/crud/config/product-state')
ns_crud.add_resource(CRUD_ConfigProductState_List, '/crud/config/product-state-list')
ns_crud.add_resource(CRUD_ConfigProductVariation, '/crud/config/product-variation/<int:id>', '/crud/config/product-variation')
ns_crud.add_resource(CRUD_ConfigProductVariation_List, '/crud/config/product-variation-list')
ns_crud.add_resource(CRUD_ConfigProductVariationState, '/crud/config/product-variation-state/<int:id>', '/crud/config/product-variation-state')
ns_crud.add_resource(CRUD_ConfigProductVariationState_List, '/crud/config/product-variation-state-list')
ns_crud.add_resource(CRUD_ConfigProvision_Product, '/crud/config/provision-product/<int:id>', '/crud/config/provision-product')
ns_crud.add_resource(CRUD_ConfigProvision_Product_List, '/crud/config/provision-product-list')
ns_crud.add_resource(CRUD_ConfigProvision_RateTable, '/crud/config/provision-rate-table/<int:id>', '/crud/config/provision-rate-table')
ns_crud.add_resource(CRUD_ConfigProvision_RateTable_List, '/crud/config/provision-rate-table-list')
ns_crud.add_resource(CRUD_ConfigProvisionState, '/crud/config/provision-state/<int:id>', '/crud/config/provision-state')
ns_crud.add_resource(CRUD_ConfigProvisionState_List, '/crud/config/provision-state-list')
ns_crud.add_resource(CRUD_ConfigProvisionUI, '/crud/config/provision-ui/<int:id>', '/crud/config/provision-ui')
ns_crud.add_resource(CRUD_ConfigProvisionUI_List, '/crud/config/provision-ui-list')
ns_crud.add_resource(CRUD_ConfigRateGroup, '/crud/config/rate-group/<int:id>', '/crud/config/rate-group')
ns_crud.add_resource(CRUD_ConfigRateGroup_List, '/crud/config/rate-group-list')
ns_crud.add_resource(CRUD_ConfigRateTable, '/crud/config/rate-table/<int:id>', '/crud/config/rate-table')
ns_crud.add_resource(CRUD_ConfigRateTable_List, '/crud/config/rate-table-list')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperDetail, '/crud/config/relationship-mapper-detail/<int:id>', '/crud/config/relationship-mapper-detail')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperDetail_List, '/crud/config/relationship-mapper-detail-list')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperSet, '/crud/config/relationship-mapper-set/<int:id>', '/crud/config/relationship-mapper-set')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperSet_List, '/crud/config/relationship-mapper-set-list')

ns_crud.add_resource(CRUD_RefAttrMapperType, '/crud/ref/attr-mapper-type/<int:id>', '/crud/ref/attr-mapper-type')
ns_crud.add_resource(CRUD_RefAttrMapperType_List, '/crud/ref/attr-mapper-type-list')
ns_crud.add_resource(CRUD_RefBenefit, '/crud/ref/benefit/<int:id>', '/crud/ref/benefit')
ns_crud.add_resource(CRUD_RefBenefit_List, '/crud/ref/benefit-list')
ns_crud.add_resource(CRUD_RefCensusStrategy, '/crud/ref/census-strategy/<int:id>', '/crud/ref/census-strategy')
ns_crud.add_resource(CRUD_RefCensusStrategy_List, '/crud/ref/census-strategy-list')
ns_crud.add_resource(CRUD_RefComparisonOperator, '/crud/ref/comparison-operator/<int:id>', '/crud/ref/comparison-operator')
ns_crud.add_resource(CRUD_RefComparisonOperator_List, '/crud/ref/comparison-operator-list')
ns_crud.add_resource(CRUD_RefComponentTypes, '/crud/ref/component-type/<int:id>', '/crud/ref/component-type')
ns_crud.add_resource(CRUD_RefComponentTypes_List, '/crud/ref/component-type-list')
ns_crud.add_resource(CRUD_RefDataTypes, '/crud/ref/data-type/<int:id>', '/crud/ref/data-type')
ns_crud.add_resource(CRUD_RefDataTypes_List, '/crud/ref/data-type-list')
ns_crud.add_resource(CRUD_RefFactorType, '/crud/ref/factor-type/<int:id>', '/crud/ref/factor-type')
ns_crud.add_resource(CRUD_RefFactorType_List, '/crud/ref/factor-type-list')
ns_crud.add_resource(CRUD_RefInputTypes, '/crud/ref/input-type/<int:id>', '/crud/ref/input-type')
ns_crud.add_resource(CRUD_RefInputTypes_List, '/crud/ref/input-type-list')
ns_crud.add_resource(CRUD_RefPremiumFrequency, '/crud/ref/premium-frequency/<int:id>', '/crud/ref/premium-frequency')
ns_crud.add_resource(CRUD_RefPremiumFrequency_List, '/crud/ref/premium-frequency-list')
ns_crud.add_resource(CRUD_RefProductVariation, '/crud/ref/product-variation/<int:id>', '/crud/ref/product-variation')
ns_crud.add_resource(CRUD_RefProductVariation_List, '/crud/ref/product-variation-list')
ns_crud.add_resource(CRUD_RefProvision, '/crud/ref/provision/<int:id>', '/crud/ref/provision')
ns_crud.add_resource(CRUD_RefProvision_List, '/crud/ref/provision-list')
ns_crud.add_resource(CRUD_RefRatingStrategy, '/crud/ref/rating-strategy/<int:id>', '/crud/ref/rating-strategy')
ns_crud.add_resource(CRUD_RefRatingStrategy_List, '/crud/ref/rating-strategy-list')
ns_crud.add_resource(CRUD_RefStates, '/crud/ref/state/<int:id>', '/crud/ref/state')
ns_crud.add_resource(CRUD_RefStates_List, '/crud/ref/state-list')
ns_crud.add_resource(CRUD_RefUnitCode, '/crud/ref/unit-code/<int:id>', '/crud/ref/unit-code')
ns_crud.add_resource(CRUD_RefUnitCode_List, '/crud/ref/unit-code-list')

ns_crud.add_resource(CRUD_SelectionAgeBand, '/crud/selection/age-band/<int:id>', '/crud/selection/age-band')
ns_crud.add_resource(CRUD_SelectionAgeBand_List, '/crud/selection/age-band-list')
ns_crud.add_resource(CRUD_SelectionBenefit, '/crud/selection/benefit/<int:id>', '/crud/selection/benefit')
ns_crud.add_resource(CRUD_SelectionBenefit_List, '/crud/selection/benefit-list')
ns_crud.add_resource(CRUD_SelectionBenefitDuration, '/crud/selection/benefit-duration/<int:id>', '/crud/selection/benefit-duration')
ns_crud.add_resource(CRUD_SelectionBenefitDuration_List, '/crud/selection/benefit-duration-list')
ns_crud.add_resource(CRUD_SelectionCensusDetail, '/crud/selection/census-detail/<int:id>', '/crud/selection/census-detail')
ns_crud.add_resource(CRUD_SelectionCensusDetail_List, '/crud/selection/census-detail-list')
ns_crud.add_resource(CRUD_SelectionCensusSet, '/crud/selection/census-set/<int:id>', '/crud/selection/census-set')
ns_crud.add_resource(CRUD_SelectionCensusSet_List, '/crud/selection/census-set-list')
ns_crud.add_resource(CRUD_SelectionPlan, '/crud/selection/plan/<int:id>', '/crud/selection/plan')
ns_crud.add_resource(CRUD_SelectionPlan_List, '/crud/selection/plan-list')
ns_crud.add_resource(CRUD_SelectionProvision, '/crud/selection/provision/<int:id>', '/crud/selection/provision')
ns_crud.add_resource(CRUD_SelectionProvision_List, '/crud/selection/provision-list')

