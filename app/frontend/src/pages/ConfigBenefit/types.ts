
export type RefBenefit = {
    ref_id: number; 
    ref_entity_code: string; 
    ref_attr_code: string; 
    ref_attr_label: string; 
    ref_attr_description?: string; 
    ref_attr_symbol?: string; 
    ref_attr_value?: number; 
}

export type RefUnitType = {
    ref_id: number; 
    ref_entity_code: string; 
    ref_attr_code: string; 
    ref_attr_label: string; 
    ref_attr_description?: string; 
    ref_attr_symbol?: string; 
    ref_attr_value?: number; 
}

export type ConfigCoverage = {
    config_coverage_id?: number | undefined | null; 
    config_product_id: number; 
    config_coverage_code: string; 
    config_coverage_label: string; 
    parent_coverage_id?: number | undefined | null; 
}

export type ConfigRateGroup = {
    config_rate_group_id?: number | undefined | null; 
    config_product_id: number; 
    config_rate_group_code: string;
    config_rate_group_label: string; 
    unit_value: number; 
    apply_discretionary_factor: boolean; 
}

export type ConfigBenefitAuthACL = {
    config_benefit_auth_acl_id?: number | undefined | null; 
    config_benefit_auth_id?: number | undefined | null; 
    auth_role_code: string;
}

export type ConfigBenefitAuth = {
    config_benefit_auth_id?: number | undefined | null;
    config_benefit_id?: number | undefined | null; 
    priority: number; 
    min_value: number; 
    max_value: number; 
    step_value: number; 
    default_value: number; 
}

export type ConfigBenefit = {
    config_benefit_id?: number;
    config_product_id: number; 
    ref_benefit_id: number; 
    ref_benefit: RefBenefit;
    config_coverage_id?: number | null | undefined;
    config_rate_group_id?: number | null | undefined;
    config_benefit_version_code: string;
    unit_type_id?: number | null | undefined;
    unit_type: RefUnitType; 
    config_benefit_description: string;
}
