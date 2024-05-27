import { z } from "zod";
import { format } from "date-fns";

export const SelectionPlanCreateNewFormSchema = z.object({
  config_product_id: z.coerce
    .number({ message: "Please select a product" })
    .positive(),
  selection_plan_effective_date: z.coerce.date({
    message: "Please select an effective date",
  }),
  situs_state_id: z.coerce
    .number({ message: "Please select a situs state" })
    .positive(),
  config_product_variation_id: z.coerce
    .number({ message: "Please select a product variation" })
    .positive(),
  selection_group_id: z.coerce.number().positive().nullable().optional(),
});

export const SelectionPlanCreateNewForm_PayloadSchema = z.object({
  config_product_id: z.coerce.number().positive(),
  selection_plan_effective_date: z.coerce
    .date()
    .transform((val) => format(val, "yyyy-MM-dd")),
  situs_state_id: z.coerce.number().positive(),
  config_product_variation_state_id: z.coerce.number().positive(),
  selection_group_id: z.coerce.number().positive().nullable().optional(),
});

export const SelectionPlan = z.object({
  selection_plan_id: z.coerce.number().positive(),
  config_product_id: z.coerce.number().positive(),
  selection_plan_effective_date: z.coerce
    .date()
    .transform((val) => format(val, "yyyy-MM-dd")),
  situs_state_id: z.coerce.number().positive(),
  config_product_variation_state_id: z.coerce.number().positive(),
  selection_group_id: z.coerce.number().positive().nullable().optional(),
});

export const SelectionPlan_APISuccessResponse = z
  .object({
    status: z.literal("success"),
    msg: z.string().optional(),
    data: SelectionPlan,
  })
  .transform((val) => val.data);
