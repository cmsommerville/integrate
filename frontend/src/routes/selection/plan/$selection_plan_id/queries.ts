import {
  SelectionBenefitList_APISuccessResponse,
  SelectableBenefitsListSchema,
} from "./schemas";

export const getSelectableBenefits = async (plan_id: number | string) => {
  const res = await fetch(`/api/dd/plan/${plan_id}/benefits`);
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  const data = await res.json();
  return SelectableBenefitsListSchema.parseAsync(data);
};

export const getSelectedBenefits = async (plan_id: number | string) => {
  const res = await fetch(`/api/selection/plan/${plan_id}/benefits`);
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  const data = await res.json();
  return SelectionBenefitList_APISuccessResponse.parseAsync(data);
};
