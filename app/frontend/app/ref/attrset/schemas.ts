import * as z from "zod";

export const AttrSetFormSchema = z.object({
  config_attr_set_id: z.number().optional(),
  config_attr_set_code: z
    .string()
    .min(2)
    .max(30)
    .regex(/[A-Za-z0-9_]/)
    .trim(),
  config_attr_set_label: z.string().min(2).max(255).trim(),
});
