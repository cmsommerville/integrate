import requests
from flask_restx import fields
from  ..models import Model_ConfigProduct, Model_RefBenefit, \
    Model_ConfigCoverage, Model_ConfigRateGroup, Model_RefUnitCode

DATA_BENEFIT = [
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cancer"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 100, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "heart_attack"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 100, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "stroke"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 100, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "renal_failure"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 100, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "transplant"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 100, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cis"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 6.25, 
        'default_value': 25, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "cabg"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 6.25, 
        'default_value': 25, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "hsb"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "FLAT"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 150, 
        'step_value': 5, 
        'default_value': 50, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "dollars"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "skin_cancer"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "base"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "FLAT"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 1000, 
        'step_value': 50, 
        'default_value': 250, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "dollars"
        }).ref_id, 
        'is_durational': True,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "ms"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "prog_benefits"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 0, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
    {
        'config_product_id': Model_ConfigProduct.find_one_by_attr({
            "config_product_code": "CI21000"
        }).config_product_id, 
        'ref_benefit_id': Model_RefBenefit.find_one_by_attr({
            "ref_attr_code": "als"
        }).ref_id, 
        'config_coverage_id': Model_ConfigCoverage.find_one_by_attr({
            "config_coverage_code": "prog_benefits"
        }).config_coverage_id, 
        'config_rate_group_id': Model_ConfigRateGroup.find_one_by_attr({
            "config_rate_group_code": "APU"
        }).config_rate_group_id,
        'min_value': 0, 
        'max_value': 100, 
        'step_value': 12.5, 
        'default_value': 0, 
        'unit_type_id': Model_RefUnitCode.find_one_by_attr({
            "ref_attr_code": "percent"
        }).ref_id, 
        'is_durational': False,
        'config_product_description': "" 
    }, 
]


def load() -> None:
    requests.post(fields.Url('CRUD_ConfigBenefit_List'), DATA_BENEFIT)


if __name__ == '__main__':
    load()