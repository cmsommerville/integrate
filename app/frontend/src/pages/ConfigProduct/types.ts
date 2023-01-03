export type ConfigProduct = {
    config_product_id: number;
    config_product_code: string;
    config_product_label: string;
    config_product_effective_date: string;
    config_product_expiration_date: string;
    product_issue_date?: string | null | undefined;
    master_product_code?: string | null | undefined;
    form_code?: string | null | undefined;
    min_issue_age?: number;
    max_issue_age?: number;
}

export type ConfigProduct_SmokerStatus = {
    smoker_status_distribution_set_id: number | null | undefined;
    smoker_status_rating_strategy_id: number | null | undefined;
    smoker_status_attr_set_id: number | null | undefined;
}

export type ConfigProduct_Gender = {
    gender_distribution_set_id: number | null | undefined;
    gender_rating_strategy_id: number | null | undefined;
    gender_attr_set_id: number | null | undefined;
}

export type ConfigProduct_Age = {
    age_distribution_set_id: number | null | undefined;
    age_rating_strategy_id: number | null | undefined;
}

export type ConfigProduct_Relationship = {
    relationship_attr_set_id: number | null | undefined;
}

export type ConfigProduct_EmployerPaid = {
    allow_employer_paid: boolean | null | undefined; 
    voluntary_census_strategy_id: number | null | undefined; 
    employer_paid_census_strategy_id: number | null | undefined; 
}

export type ConfigAttributeDetail = {
    config_attr_detail_id: number; 
    config_attr_set_id: number; 
    config_attr_detail_code: string; 
    config_attr_detail_label: string; 
    is_composite_id: boolean;
}

export type ConfigAttributeSet = {
    config_attr_set_id: number; 
    config_attr_type_code: string; 
    config_attr_set_label: string; 
    attributes: ConfigAttributeDetail[];
}

export type ConfigAttributeDistributionDetail = {
    config_attr_distribution_id: number; 
    config_attr_distribution_set_id: number; 
    config_attr_detail_id: number; 
    weight: number; 
}

export type ConfigAttributeDistributionSet_Gender = {
    config_attr_distribution_set_id: number; 
    config_attr_type_code: string; 
    config_attr_distribution_set_label: string; 
    gender_distribution: ConfigAttributeDistributionDetail[]
}

export type ConfigAttributeDistributionSet_SmokerStatus = {
    config_attr_distribution_set_id: number; 
    config_attr_type_code: string; 
    config_attr_distribution_set_label: string; 
    smoker_status_distribution: ConfigAttributeDistributionDetail[]
}

export type RefRatingStrategy = {
    ref_id: number; 
    ref_entity_code: string; 
    ref_attr_code: string; 
    ref_attr_label: string; 
    ref_attr_description?: string; 
    ref_attr_symbol?: string; 
    ref_attr_value?: number; 
}
