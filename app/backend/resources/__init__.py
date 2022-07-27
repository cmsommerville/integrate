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
from .Config_Provision import CRUD_ConfigProvision, CRUD_ConfigProvision_List
from .Config_ProvisionState import CRUD_ConfigProvisionState, CRUD_ConfigProvisionState_List
from .Config_ProvisionUI import CRUD_ConfigProvisionUI, CRUD_ConfigProvisionUI_List
from .Config_RateGroup import CRUD_ConfigRateGroup, CRUD_ConfigRateGroup_List
from .Config_RelationshipMapperDetail import CRUD_ConfigRelationshipMapperDetail, CRUD_ConfigRelationshipMapperDetail_List
from .Config_RelationshipMapperSet import CRUD_ConfigRelationshipMapperSet, CRUD_ConfigRelationshipMapperSet_List
# from .Ref_Master import *
from .Ref_States import CRUD_RefStates, CRUD_RefStates_List

ns_crud = Namespace("crud", "Namespace containing standard CRUD endpoints")

ns_crud.add_resource(CRUD_ConfigAgeBandDetail, '/crud/config/age-band-detail/<int:id>', '/crud/config/age-band-detail', endpoint='CRUD_ConfigAgeBandDetail')
ns_crud.add_resource(CRUD_ConfigAgeBandDetail_List, '/crud/config/age-band-detail-list', endpoint='CRUD_ConfigAgeBandDetail_List')
ns_crud.add_resource(CRUD_ConfigAgeBandSet, '/crud/config/age-band-set/<int:id>', '/crud/config/age-band-set', endpoint='CRUD_ConfigAgeBandSet')
ns_crud.add_resource(CRUD_ConfigAgeBandSet_List, '/crud/config/age-band-set-list', endpoint='CRUD_ConfigAgeBandSet_List')
ns_crud.add_resource(CRUD_ConfigAgeDistribution, '/crud/config/age-distribution/<int:id>', '/crud/config/age-distribution', endpoint='CRUD_ConfigAgeDistribution')
ns_crud.add_resource(CRUD_ConfigAgeDistribution_List, '/crud/config/age-distribution-list', endpoint='CRUD_ConfigAgeDistribution_List')
ns_crud.add_resource(CRUD_ConfigAgeDistributionSet, '/crud/config/age-distribution-set/<int:id>', '/crud/config/age-distribution-set', endpoint='CRUD_ConfigAgeDistributionSet')
ns_crud.add_resource(CRUD_ConfigAgeDistributionSet_List, '/crud/config/age-distribution-set-list', endpoint='CRUD_ConfigAgeDistributionSet_List')
ns_crud.add_resource(CRUD_ConfigAgeMapperDetail, '/crud/config/age-mapper-detail/<int:id>', '/crud/config/age-mapper-detail', endpoint='CRUD_ConfigAgeMapperDetail')
ns_crud.add_resource(CRUD_ConfigAgeMapperDetail_List, '/crud/config/age-mapper-detail-list', endpoint='CRUD_ConfigAgeMapperDetail_List')
ns_crud.add_resource(CRUD_ConfigAttributeDetail, '/crud/config/attribute-detail/<int:id>', '/crud/config/attribute-detail', endpoint='CRUD_ConfigAttributeDetail')
ns_crud.add_resource(CRUD_ConfigAttributeDetail_List, '/crud/config/attribute-detail-list', endpoint='CRUD_ConfigAttributeDetail_List')
ns_crud.add_resource(CRUD_ConfigAttributeDistribution, '/crud/config/attribute-distribution/<int:id>', '/crud/config/attribute-distribution', endpoint='CRUD_ConfigAttributeDistribution')
ns_crud.add_resource(CRUD_ConfigAttributeDistribution_List, '/crud/config/attribute-distribution-list', endpoint='CRUD_ConfigAttributeDistribution_List')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_Gender, '/crud/config/attribute-distribution-set-gender/<int:id>', '/crud/config/attribute-distribution-set-gender', endpoint='CRUD_ConfigAttributeDistributionSet_Gender')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_Gender_List, '/crud/config/attribute-distribution-set-gender-list', endpoint='CRUD_ConfigAttributeDistributionSet_Gender_List')
ns_crud.add_resource(CRUD_ConfigAttributeDistributionSet_SmokerStatus, '/crud/config/attribute-distribution-set-smoker-status/<int:id>', '/crud/config/attribute-distribution-set-smoker-status', endpoint='CRUD_ConfigAttributeDistributionSet_SmokerStatus')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Gender, '/crud/config/attribute-set-gender/<int:id>', '/crud/config/attribute-set-gender', endpoint='CRUD_ConfigAttributeSet_Gender')
ns_crud.add_resource(CRUD_ConfigAttributeSet_SmokerStatus, '/crud/config/attribute-set-smoker-status/<int:id>', '/crud/config/attribute-set-smoker-status', endpoint='CRUD_ConfigAttributeSet_SmokerStatus')
ns_crud.add_resource(CRUD_ConfigAttributeSet_Relationship, '/crud/config/attribute-set-relationship/<int:id>', '/crud/config/attribute-set-relationship', endpoint='CRUD_ConfigAttributeSet_Relationship')
ns_crud.add_resource(CRUD_ConfigBenefit, '/crud/config/benefit/<int:id>', '/crud/config/benefit', endpoint='CRUD_ConfigBenefit')
ns_crud.add_resource(CRUD_ConfigBenefit_List, '/crud/config/benefit-list', endpoint='CRUD_ConfigBenefit_List')
ns_crud.add_resource(CRUD_ConfigBenefitDurationDetail, '/crud/config/benefit-duration-detail/<int:id>', '/crud/config/benefit-duration-detail', endpoint='CRUD_ConfigBenefitDurationDetail')
ns_crud.add_resource(CRUD_ConfigBenefitDurationDetail_List, '/crud/config/benefit-duration-detail-list', endpoint='CRUD_ConfigBenefitDurationDetail_List')
ns_crud.add_resource(CRUD_ConfigBenefitDurationSet, '/crud/config/benefit-duration-set/<int:id>', '/crud/config/benefit-duration-set', endpoint='CRUD_ConfigBenefitDurationSet')
ns_crud.add_resource(CRUD_ConfigBenefitDurationSet_List, '/crud/config/benefit-duration-set-list', endpoint='CRUD_ConfigBenefitDurationSet_List')
ns_crud.add_resource(CRUD_ConfigBenefitState, '/crud/config/benefit-state/<int:id>', '/crud/config/benefit-state', endpoint='CRUD_ConfigBenefitState')
ns_crud.add_resource(CRUD_ConfigBenefitState_List, '/crud/config/benefit-state-list', endpoint='CRUD_ConfigBenefitState_List')
ns_crud.add_resource(CRUD_ConfigCoverage, '/crud/config/coverage/<int:id>', '/crud/config/coverage', endpoint='CRUD_ConfigCoverage')
ns_crud.add_resource(CRUD_ConfigCoverage_List, '/crud/config/coverage-list', endpoint='CRUD_ConfigCoverage_List')
ns_crud.add_resource(CRUD_ConfigFactor, '/crud/config/factor/<int:id>', '/crud/config/factor', endpoint='CRUD_ConfigFactor')
ns_crud.add_resource(CRUD_ConfigFactor_List, '/crud/config/factor-list', endpoint='CRUD_ConfigFactor_List')
ns_crud.add_resource(CRUD_ConfigFactorRule, '/crud/config/factor-rule/<int:id>', '/crud/config/factor-rule', endpoint='CRUD_ConfigFactorRule')
ns_crud.add_resource(CRUD_ConfigFactorRule_List, '/crud/config/factor-rule-list', endpoint='CRUD_ConfigFactorRule_List')
ns_crud.add_resource(CRUD_ConfigProduct, '/crud/config/product/<int:id>', '/crud/config/product', endpoint='CRUD_ConfigProduct')
ns_crud.add_resource(CRUD_ConfigProduct_List, '/crud/config/product-list', endpoint='CRUD_ConfigProduct_List')
ns_crud.add_resource(CRUD_ConfigProductMapperDetail, '/crud/config/product-mapper-detail/<int:id>', '/crud/config/product-mapper-detail', endpoint='CRUD_ConfigProductMapperDetail')
ns_crud.add_resource(CRUD_ConfigProductMapperDetail_List, '/crud/config/product-mapper-detail-list', endpoint='CRUD_ConfigProductMapperDetail_List')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_Gender, '/crud/config/product-mapper-set-gender/<int:id>', '/crud/config/product-mapper-set-gender', endpoint='CRUD_ConfigProductMapperSet_Gender')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_Gender_List, '/crud/config/product-mapper-set-gender-list', endpoint='CRUD_ConfigProductMapperSet_Gender_List')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_SmokerStatus, '/crud/config/product-mapper-set-smoker-status/<int:id>', '/crud/config/product-mapper-set-smoker-status', endpoint='CRUD_ConfigProductMapperSet_SmokerStatus')
ns_crud.add_resource(CRUD_ConfigProductMapperSet_SmokerStatus_List, '/crud/config/product-mapper-set-smoker-status-list', endpoint='CRUD_ConfigProductMapperSet_SmokerStatus_List')
ns_crud.add_resource(CRUD_ConfigProductState, '/crud/config/product-state/<int:id>', '/crud/config/product-state', endpoint='CRUD_ConfigProductState')
ns_crud.add_resource(CRUD_ConfigProductState_List, '/crud/config/product-state-list', endpoint='CRUD_ConfigProductState_List')
ns_crud.add_resource(CRUD_ConfigProductVariation, '/crud/config/product-variation/<int:id>', '/crud/config/product-variation', endpoint='CRUD_ConfigProductVariation')
ns_crud.add_resource(CRUD_ConfigProductVariation_List, '/crud/config/product-variation-list', endpoint='CRUD_ConfigProductVariation_List')
ns_crud.add_resource(CRUD_ConfigProductVariationState, '/crud/config/product-variation-state/<int:id>', '/crud/config/product-variation-state', endpoint='CRUD_ConfigProductVariationState')
ns_crud.add_resource(CRUD_ConfigProductVariationState_List, '/crud/config/product-variation-state-list', endpoint='CRUD_ConfigProductVariationState_List')
ns_crud.add_resource(CRUD_ConfigProvision, '/crud/config/provision/<int:id>', '/crud/config/provision', endpoint='CRUD_ConfigProvision')
ns_crud.add_resource(CRUD_ConfigProvision_List, '/crud/config/provision-list', endpoint='CRUD_ConfigProvision_List')
ns_crud.add_resource(CRUD_ConfigProvisionState, '/crud/config/provision-state/<int:id>', '/crud/config/provision-state', endpoint='CRUD_ConfigProvisionState')
ns_crud.add_resource(CRUD_ConfigProvisionState_List, '/crud/config/provision-state-list', endpoint='CRUD_ConfigProvisionState_List')
ns_crud.add_resource(CRUD_ConfigProvisionUI, '/crud/config/provision-ui/<int:id>', '/crud/config/provision-ui', endpoint='CRUD_ConfigProvisionUI')
ns_crud.add_resource(CRUD_ConfigProvisionUI_List, '/crud/config/provision-ui-list', endpoint='CRUD_ConfigProvisionUI_List')
ns_crud.add_resource(CRUD_ConfigRateGroup, '/crud/config/rate-group/<int:id>', '/crud/config/rate-group', endpoint='CRUD_ConfigRateGroup')
ns_crud.add_resource(CRUD_ConfigRateGroup_List, '/crud/config/rate-group-list', endpoint='CRUD_ConfigRateGroup_List')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperDetail, '/crud/config/relationship-mapper-detail/<int:id>', '/crud/config/relationship-mapper-detail', endpoint='CRUD_ConfigRelationshipMapperDetail')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperDetail_List, '/crud/config/relationship-mapper-detail-list', endpoint='CRUD_ConfigRelationshipMapperDetail_List')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperSet, '/crud/config/relationship-mapper-set/<int:id>', '/crud/config/relationship-mapper-set', endpoint='CRUD_ConfigRelationshipMapperSet')
ns_crud.add_resource(CRUD_ConfigRelationshipMapperSet_List, '/crud/config/relationship-mapper-set-list', endpoint='CRUD_ConfigRelationshipMapperSet_List')
