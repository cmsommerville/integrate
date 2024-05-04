import * as z from "zod";
import { isDate } from "date-fns";

export const ProductFormSchema = z.object({
  config_product_id: z.number().optional(),
  config_product_code: z
    .string()
    .min(2)
    .max(30)
    .regex(/[A-Za-z0-9_]/)
    .trim(),
  config_product_label: z.string().min(2).max(255).trim(),
  form_code: z.string().min(2).trim(),
  config_product_effective_date: z.string().refine((val) => isDate(val), {
    message: "Must be a valid date in string format",
  }),
  config_product_expiration_date: z.string().refine((val) => isDate(val), {
    message: "Must be a valid date in string format",
  }),
});
