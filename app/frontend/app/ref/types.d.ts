export type NewConfigAttributeSet = {
  config_attr_set_code: string;
  config_attr_set_label: string;
};
export type ConfigAttributeSet = {
  config_attr_set_id: number;
} & NewConfigAttributeSet;

export type NewConfigAttributeDetail = {
  config_attr_detail_code: string;
  config_attr_detail_label: string;
  config_attr_set_id: number;
};
export type ConfigAttributeDetail = {
  config_attr_detail_id: number;
} & NewConfigAttributeSet;
