import * as z from "zod";

export const RatingMapperCollectionFormSchema = z.object({
  config_rating_mapper_collection_id: z.number().optional(),
  config_attribute_set_id: z.coerce.number(),
  config_rating_mapper_collection_label: z.string().min(2).max(255).trim(),
  default_config_rating_mapper_set_id: z.coerce.number().optional(),
  is_selectable: z.boolean().default(false),
});

export const RatingMapperSetFormSchema = z.object({
  config_rating_mapper_set_id: z.number().optional(),
  config_rating_mapper_collection_id: z.coerce.number(),
  config_rating_mapper_set_label: z.string().min(2).max(255).trim(),
  is_composite: z.boolean().default(false),
  is_employer_paid: z.boolean().default(false),
});
