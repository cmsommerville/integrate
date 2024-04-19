import * as z from "zod";
import { isDate } from "date-fns";

export const ProductVariationFormSchema = z.object({
  config_product_variation_id: z.number().optional(),
  config_product_id: z.number(),
  config_product_variation_version_code: z
    .string()
    .min(2)
    .max(30)
    .regex(/[A-Za-z0-9_]/)
    .trim(),
});
