export type ConfigProduct_Basic = {
    config_product_id: number;
    config_product_code: string;
    config_product_label: string;
    config_product_effective_date: string;
    config_product_expiration_date: string;
    product_issue_date?: string | undefined;
    master_product_code?: string | undefined;
    form_code?: string | undefined;
    min_issue_age?: number;
    max_issue_age?: number;
}

export type ConfigProduct_AttrSets = {
    smoker_status_attr_set_id: number | undefined;
    gender_attr_set_id: number | undefined;
    relationship_attr_set_id: number | undefined;
}

export type ConfigProduct_DistributionSets = {
    smoker_status_distribution_set_id: number | undefined;
    gender_distribution_set_id: number | undefined;
    age_distribution_set_id: number | undefined;
}

export type ConfigProduct_RatingStrategies = {
    smoker_status_rating_strategy_id: number | undefined;
    gender_rating_strategy_id: number | undefined;
    age_rating_strategy_id: number | undefined;
}

export type ConfigProduct_EmployerPaid = {
    allow_employer_paid: boolean | undefined; 
    voluntary_census_strategy_id: number | undefined; 
    employer_paid_census_strategy_id: number | undefined; 
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

export type ConfigAgeDistributionDetail = {
    config_age_distribution_id: number; 
    config_age_distribution_set_id: number; 
    age_value: number; 
    weight: number;
}

export type ConfigAgeDistributionSet = {
    config_age_distribution_set_id: number; 
    config_age_distribution_set_label: string;
    age_distribution: ConfigAgeDistributionDetail[];
}
