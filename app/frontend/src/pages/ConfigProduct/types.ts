export type Product = {
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