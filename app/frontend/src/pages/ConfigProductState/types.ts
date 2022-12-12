import {StateSVG} from '@/components/Map'

export interface ConfigProductStateType {
    config_product_state_id: number; 
    config_product_id: number; 
    state_id: number; 
    config_product_state_effective_date: string; 
    config_product_state_expiration_date: string; 
    state: StateSVG;
}
