export interface StateSVG {
    state_id: number; 
    state_code: string; 
    state_name: string;
    svg_path: string; 
    created_dts?: string | null | undefined;
    updated_dts?: string | null | undefined;
    updated_by?: string | null | undefined; 
}