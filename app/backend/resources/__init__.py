from flask_restx import Namespace

from .TestResource import TestResource
from .Config_AgeBandDetail import (
    CRUD_ConfigAgeBandDetail,
    CRUD_ConfigAgeBandDetail_List,
)
from .Config_AgeBandSet import CRUD_ConfigAgeBandSet, CRUD_ConfigAgeBandSet_List
from .Config_AgeDistribution import (
    CRUD_ConfigAgeDistribution,
    CRUD_ConfigAgeDistribution_List,
)
from .Config_AgeDistributionSet import (
    CRUD_ConfigAgeDistributionSet,
    CRUD_ConfigAgeDistributionSet_List,
)
from .Config_AttributeDetail import (
    CRUD_ConfigAttributeDetail,
    CRUD_ConfigAttributeDetail_List,
)
from .Config_AttributeSet import (
    CRUD_ConfigAttributeSet,
    CRUD_ConfigAttributeSet_List,
)
from .Config_Benefit import (
    CRUD_ConfigBenefit,
    CRUD_ConfigBenefit_List,
    Data_ConfigBenefit,
    Data_ConfigBenefit_List,
)
from .Config_BenefitDurationDetail import (
    CRUD_ConfigBenefitDurationDetail,
    CRUD_ConfigBenefitDurationDetail_List,
)
from .Config_BenefitDurationSet import (
    CRUD_ConfigBenefitDurationSet,
    CRUD_ConfigBenefitDurationSet_List,
)
from .Config_BenefitProvision import (
    CRUD_ConfigBenefitProvision,
    CRUD_ConfigBenefitProvision_List,
)
from .Config_BenefitVariationState import (
    CRUD_ConfigBenefitVariationState,
    CRUD_ConfigBenefitVariationState_List,
    ConfigBenefitVariationStateRateset,
)
from .Config_Coverage import CRUD_ConfigCoverage, CRUD_ConfigCoverage_List
from .Config_DropdownDetail import (
    CRUD_ConfigDropdownDetail,
    CRUD_ConfigDropdownDetail_List,
)
from .Config_DropdownSet import CRUD_ConfigDropdownSet, CRUD_ConfigDropdownSet_List
from .Config_Factor import CRUD_ConfigFactorSet, CRUD_ConfigFactorSet_List
from .Config_FactorRule import CRUD_ConfigFactorRule, CRUD_ConfigFactorRule_List
from .Config_PlanDesignDetail import (
    CRUD_ConfigPlanDesignDetail_Benefit,
    CRUD_ConfigPlanDesignDetail_Benefit_List,
    CRUD_ConfigPlanDesignDetail_PlanDesign,
    CRUD_ConfigPlanDesignDetail_PlanDesign_List,
)
from .Config_PlanDesignSet import (
    CRUD_ConfigPlanDesignSet_Coverage,
    CRUD_ConfigPlanDesignSet_Coverage_List,
    CRUD_ConfigPlanDesignSet_Product,
    CRUD_ConfigPlanDesignSet_Product_List,
)
from .Config_PlanDesignVariationState import (
    CRUD_ConfigPlanDesignVariationState,
    CRUD_ConfigPlanDesignVariationState_List,
    Resource_ConfigPlanDesignVariationState_CoveragePlanDesignList,
    Resource_ConfigPlanDesignVariationState_ProductPlanDesignList,
)
from .Config_Product import (
    CRUD_ConfigProduct,
    CRUD_ConfigProduct_List,
    Progress_ConfigProduct,
)
from .Config_ProductState import CRUD_ConfigProductState, CRUD_ConfigProductState_List
from .Config_ProductVariation import (
    CRUD_ConfigProductVariation,
    CRUD_ConfigProductVariation_List,
    Resource_ConfigProductVariation_SetPlanDesignVariationStates,
)
from .Config_ProductVariationState import (
    CRUD_ConfigProductVariationState,
    CRUD_ConfigProductVariationState_List,
)
from .Config_Provision import CRUD_ConfigProvision, CRUD_ConfigProvision_List
from .Config_ProvisionState import (
    CRUD_ConfigProvisionState,
    CRUD_ConfigProvisionState_List,
)
from .Config_ProvisionUI import CRUD_ConfigProvisionUI, CRUD_ConfigProvisionUI_List
from .Config_RateGroup import CRUD_ConfigRateGroup, CRUD_ConfigRateGroup_List
from .Config_RateTable import (
    CRUD_ConfigRateTable,
    CRUD_ConfigRateTable_List,
    CRUD_ConfigRateTableSet,
    CRUD_ConfigRateTableSet_List,
    RateTableCohortsResource,
)
from .Config_RatingMapperCollection import (
    CRUD_ConfigRatingMapperCollection,
    CRUD_ConfigRatingMapperCollection_List,
)
from .Config_RatingMapperSet import (
    CRUD_ConfigRatingMapperSet,
    CRUD_ConfigRatingMapperSet_List,
)
from .Config_RatingMapperDetail import (
    CRUD_ConfigRatingMapperDetail,
    CRUD_ConfigRatingMapperDetail_List,
)
from .Ref_Master import *
from .Ref_States import CRUD_RefStates, CRUD_RefStates_List


from .Selection_RPC import Resource_Selection_RPC_Dispatcher
from .Selection_AgeBand import CRUD_SelectionAgeBand, CRUD_SelectionAgeBand_List
from .Selection_Benefit import (
    CRUD_SelectionBenefit,
    CRUD_SelectionBenefit_List,
)
from .Selection_BenefitDuration import (
    CRUD_SelectionBenefitDuration,
    CRUD_SelectionBenefitDuration_List,
)
from .Selection_Coverage import (
    CRUD_SelectionCoverage,
    CRUD_SelectionCoverage_List,
)
from .Selection_Plan import (
    CRUD_SelectionPlan,
    CRUD_SelectionPlan_List,
    CRUD_SelectionPlan_CreateOnly,
)
from .Selection_Provision import (
    CRUD_SelectionProvision,
    CRUD_SelectionProvision_List,
    CRUD_SelectionProvision_CreateOnly,
)
from .Selection_RatingMapperDetail import (
    CRUD_SelectionRatingMapperDetail,
    CRUD_SelectionRatingMapperDetail_List,
)
from .Selection_RatingMapperSet import (
    CRUD_SelectionRatingMapperSet,
    CRUD_SelectionRatingMapperSet_List,
)

from .Diagnostics_ConfigProductVariationState import (
    Resource_Diagnostics_ConfigProductVariationState,
    Resource_Diagnostics_ConfigProductVariation,
)
