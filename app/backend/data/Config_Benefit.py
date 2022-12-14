import requests
from requests.compat import urljoin
from  ..models import Model_ConfigProduct, Model_RefBenefit, \
    Model_ConfigCoverage, Model_ConfigRateGroup, Model_RefUnitCode


def PRODUCT_ID(): 
    return  Model_ConfigProduct.find_one_by_attr({
        "config_product_code": "CI21000"
    }).config_product_id


def DATA_BENEFIT(product_id):
    return [
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cancer"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_cancer', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "heart_attack"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_heart_attack', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "stroke"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_stroke', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "renal_failure"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_renal_failure', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "transplant"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_transplant', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cis"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_cis', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cabg"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_cabg', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "hsb"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "FLAT"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_hsb', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "dollars"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "skin_cancer"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "FLAT"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_skin_cancer', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 500, 
                'step_value': 25, 
                'default_value': 250, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 1000, 
                'step_value': 25, 
                'default_value': 500, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "dollars"
        }).ref_id, 
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "ms"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "prog_benefits"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_ms', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
    {
        'config_product_id': product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "als"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "prog_benefits"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'config_benefit_version_code': 'std_als', 
        'benefit_auth': [
            {
                'priority': 10, 
                'min_value': 0, 
                'max_value': 25, 
                'step_value': 12.5, 
                'default_value': 25, 
                'acl': [
                    {
                        'auth_role_code': 'uw900'
                    }
                ]
            }, 
            {
                'priority': 20, 
                'min_value': 0, 
                'max_value': 100, 
                'step_value': 12.5, 
                'default_value': 100, 
                'acl': [
                    {
                        'auth_role_code': 'uw1000'
                    }
                ]
            }, 
        ], 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        
        'config_benefit_description': "" 
    }, 
]

def load(hostname: str, *args, **kwargs) -> None:
    product_id = PRODUCT_ID()
    url = urljoin(hostname, f'api/config/product/{product_id}/benefits')
    res = requests.post(url, json=DATA_BENEFIT(product_id), **kwargs)
    if not res.ok: 
        raise Exception(res.text)