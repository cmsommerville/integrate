import { DateTime } from "luxon";

export type BaseProductType = {
  config_product_code: string;
  config_product_label: string;
  form_code: string;
  config_product_effective_date: string;
  config_product_expiration_date: string;
};

export type ProductType = {
  config_product_id: number;
} & BaseProductType;

export type RefProductVariationType = {
  ref_id: number;
  ref_attr_code: string;
  ref_attr_label: string;
};

export type BaseProductVariationType = {
  config_product_id: number;
  config_product_variation_code: string;
  config_product_variation_label: string;
};

export type ProductVariationType = {
  config_product_variation_id: number;
  ref_product_variation: RefProductVariationType;
} & BaseProductVariationType;

export type NewRatingMapperCollectionType = {
  config_attribute_set_id: number;
  config_rating_mapper_collection_label: string;
  default_config_rating_mapper_set_id: number | undefined;
  is_selectable: boolean;
};

export type RatingMapperCollectionType = {
  config_rating_mapper_collection_id: number;
} & NewRatingMapperCollectionType;
