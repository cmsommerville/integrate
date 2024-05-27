import { z } from "zod";

export const SelectionBenefitDurationSchema = z.object({
  selection_benefit_duration_id: z.coerce.number(),
  selection_benefit_id: z.coerce.number(),
  config_benefit_duration_set_id: z.coerce.number(),
  config_benefit_duration_detail_id: z.coerce.number(),
  selection_factor: z.coerce.number(),
  version_id: z.coerce.string(),
  updated_dts: z.coerce.string(),
  updated_by: z.coerce.string(),
  row_eff_dts: z.coerce.string(),
  row_exp_dts: z.coerce.string(),
});

export const SelectionBenefitSchema = z.object({
  selection_benefit_id: z.coerce.number(),
  selection_plan_id: z.coerce.number(),
  selection_coverage_id: z.coerce.number(),
  config_benefit_variation_state_id: z.coerce.number(),
  selection_value: z.coerce.number(),
  duration_sets: z.array(SelectionBenefitDurationSchema),
  version_id: z.coerce.string(),
  updated_dts: z.coerce.string(),
  updated_by: z.coerce.string(),
  row_eff_dts: z.coerce.string(),
  row_exp_dts: z.coerce.string(),
});

export const SelectionBenefitListSchema = z.array(SelectionBenefitSchema);

export const SelectionBenefitList_APISuccessResponse = z
  .object({
    status: z.literal("success"),
    msg: z.string().optional(),
    data: SelectionBenefitListSchema,
  })
  .transform((val) => val.data);

export const SelectableBenefitDurationDetailSchema = z.object({
  config_benefit_duration_detail_id: z.coerce.number(),
  config_benefit_duration_detail_code: z.coerce.string(),
  config_benefit_duration_detail_label: z.coerce.string(),
  config_benefit_duration_factor: z.coerce.number(),
});

export const SelectableBenefitDurationSetSchema = z.object({
  config_benefit_duration_set_id: z.coerce.number(),
  config_benefit_duration_set_code: z.coerce.string(),
  config_benefit_duration_set_label: z.coerce.string(),
  duration_items: z.array(SelectableBenefitDurationDetailSchema),
});

export const SelectableBenefitsSchema = z.object({
  config_benefit_variation_state_id: z.coerce.number(),
  config_product_variation_state_id: z.coerce.number(),
  config_benefit_id: z.coerce.number(),
  config_benefit_variation_state_effective_date: z.coerce.string(),
  config_benefit_variation_state_expiration_date: z.coerce.string(),
  config_benefit_code: z.coerce.string(),
  config_benefit_label: z.coerce.string(),
  min_value: z.coerce.number(),
  max_value: z.coerce.number(),
  step_value: z.coerce.number(),
  durations: z.array(SelectableBenefitDurationSetSchema),
});

export const SelectableBenefitsListSchema = z.array(SelectableBenefitsSchema);
