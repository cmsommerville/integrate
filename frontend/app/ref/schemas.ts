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

export const AttrDetailFormSchema = z.object({
  config_attr_detail_id: z.coerce.number().optional(),
  config_attr_set_id: z.coerce.number().optional(),
  config_attr_detail_code: z
    .string()
    .min(1)
    .max(30)
    .regex(/[A-Za-z0-9_]/)
    .trim(),
  config_attr_detail_label: z.string().min(2).max(255).trim(),
});

export const EditAttrDetailFormSchema = z.object({
  config_attr_detail_id: z.coerce.number(),
  config_attr_set_id: z.coerce.number(),
  config_attr_detail_code: z
    .string()
    .min(1)
    .max(30)
    .regex(/[A-Za-z0-9_]/)
    .trim(),
  config_attr_detail_label: z.string().min(2).max(255).trim(),
  version_id: z.string().min(26).max(26).trim(),
});
