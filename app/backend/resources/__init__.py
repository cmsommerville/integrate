from flask_restx import Namespace

from .Config_AgeBandDetail import CRUD_ConfigAgeBandDetail, CRUD_ConfigAgeBandDetail_List
from .Config_AgeBandSet import CRUD_ConfigAgeBandSet, CRUD_ConfigAgeBandSet_List
from .Config_AgeDistribution import CRUD_ConfigAgeDistribution, CRUD_ConfigAgeDistribution_List
from .Config_AgeDistributionSet import CRUD_ConfigAgeDistributionSet, CRUD_ConfigAgeDistributionSet_List
from .Config_AgeMapperDetail import  CRUD_ConfigAgeMapperDetail, CRUD_ConfigAgeMapperDetail_List
from .Config_AttributeDetail import CRUD_ConfigAttributeDetail, CRUD_ConfigAttributeDetail_List
from .Config_AttributeDistribution import CRUD_ConfigAttributeDistribution, CRUD_ConfigAttributeDistribution_List
from .Config_AttributeDistributionSet import CRUD_ConfigAttributeDistributionSet_Gender, CRUD_ConfigAttributeDistributionSet_Gender_List, \
    CRUD_ConfigAttributeDistributionSet_SmokerStatus, CRUD_ConfigAttributeDistributionSet_SmokerStatus_List, \
    CRUD_ConfigAttributeDistributionSet, CRUD_ConfigAttributeDistributionSet_List
from .Config_AttributeSet import CRUD_ConfigAttributeSet_Gender, CRUD_ConfigAttributeSet_SmokerStatus, CRUD_ConfigAttributeSet_Relationship,  \
    CRUD_ConfigAttributeSet_Gender_List, CRUD_ConfigAttributeSet_SmokerStatus_List, CRUD_ConfigAttributeSet_Relationship_List, \
    CRUD_ConfigAttributeSet, CRUD_ConfigAttributeSet_List, CRUD_ConfigAttributeSet_NoJoin, CRUD_ConfigAttributeSet_NoJoin_List
from .Config_Benefit import CRUD_ConfigBenefit, CRUD_ConfigBenefit_List, Data_ConfigBenefit, Data_ConfigBenefit_List
from .Config_BenefitCovarianceDetail import CRUD_ConfigBenefitCovarianceDetail, CRUD_ConfigBenefitCovarianceDetail_List
from .Config_BenefitCovarianceSet import CRUD_ConfigBenefitCovarianceSet, CRUD_ConfigBenefitCovarianceSet_List
from .Config_BenefitDurationDetail import CRUD_ConfigBenefitDurationDetail, CRUD_ConfigBenefitDurationDetail_List
from .Config_BenefitDurationSet import CRUD_ConfigBenefitDurationSet, CRUD_ConfigBenefitDurationSet_List
from .Config_BenefitProductVariation import CRUD_ConfigBenefitProductVariation, CRUD_ConfigBenefitProductVariation_List
from .Config_BenefitProvision import CRUD_ConfigBenefitProvision, CRUD_ConfigBenefitProvision_List
from .Config_BenefitState import CRUD_ConfigBenefitState, CRUD_ConfigBenefitState_List
from .Config_Coverage import CRUD_ConfigCoverage, CRUD_ConfigCoverage_List 
from .Config_Factor import CRUD_ConfigFactor, CRUD_ConfigFactor_List
from .Config_FactorRule import CRUD_ConfigFactorRule, CRUD_ConfigFactorRule_List
from .Config_Product import CRUD_ConfigProduct, CRUD_ConfigProduct_List, Progress_ConfigProduct
from .Config_ProductMapperDetail import CRUD_ConfigProductMapperDetail, CRUD_ConfigProductMapperDetail_List
from .Config_ProductMapperSet import CRUD_ConfigProductMapperSet_Gender, CRUD_ConfigProductMapperSet_Gender_List, \
    CRUD_ConfigProductMapperSet_SmokerStatus, CRUD_ConfigProductMapperSet_SmokerStatus_List, \
    CRUD_ConfigProductMapperSet, CRUD_ConfigProductMapperSet_List
from .Config_ProductState import CRUD_ConfigProductState, CRUD_ConfigProductState_List
from .Config_ProductVariation import CRUD_ConfigProductVariation, CRUD_ConfigProductVariation_List
from .Config_ProductVariationState import CRUD_ConfigProductVariationState, CRUD_ConfigProductVariationState_List
from .Config_Provision import CRUD_ConfigProvision, CRUD_ConfigProvision_List
from .Config_ProvisionState import CRUD_ConfigProvisionState, CRUD_ConfigProvisionState_List
from .Config_ProvisionUI import CRUD_ConfigProvisionUI, CRUD_ConfigProvisionUI_List
from .Config_RateGroup import CRUD_ConfigRateGroup, CRUD_ConfigRateGroup_List
from .Config_RateGroupFaceAmounts import CRUD_ConfigRateGroupFaceAmounts_List
from .Config_RateTable import CRUD_ConfigRateTable, CRUD_ConfigRateTable_List
from .Config_RelationshipMapperDetail import CRUD_ConfigRelationshipMapperDetail, CRUD_ConfigRelationshipMapperDetail_List
from .Config_RelationshipMapperSet import CRUD_ConfigRelationshipMapperSet, CRUD_ConfigRelationshipMapperSet_List
from .Ref_Master import *
from .Ref_States import CRUD_RefStates, CRUD_RefStates_List

from .Selection_AgeBand import CRUD_SelectionAgeBand, CRUD_SelectionAgeBand_List
from .Selection_Benefit import CRUD_SelectionBenefit, CRUD_SelectionBenefit_List
from .Selection_BenefitDuration import CRUD_SelectionBenefitDuration, CRUD_SelectionBenefitDuration_List
from .Selection_BenefitRateTable import CRUD_SelectionBenefitRateTable
from .Selection_CensusDetail import CRUD_SelectionCensusDetail, CRUD_SelectionCensusDetail_List
from .Selection_CensusSet import CRUD_SelectionCensusSet, CRUD_SelectionCensusSet_List, \
    SelectionCensusSet_CensusBuilder, SelectionCensusSet_UploadFile, SelectionCensusSet_Dropdown
from .Selection_Plan import CRUD_SelectionPlan, CRUD_SelectionPlan_List, Resource_SelectionPlan_ConfigProduct, \
    Resource_SelectionPlan_GenderProductMapper, Resource_SelectionPlan_SmokerStatusProductMapper
from .Selection_Provision import CRUD_SelectionProvision, CRUD_SelectionProvision_List
from .Selection_RateGroupFaceAmounts import CRUD_SelectionRateGroupFaceAmounts, CRUD_SelectionRateGroupFaceAmounts_List
from .Selection_RateTable import Resource_SelectionRateTable

from .Rating_PremiumCalculator import Resource_RatingPremiumCalculator