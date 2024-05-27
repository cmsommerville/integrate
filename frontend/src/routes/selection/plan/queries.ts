import { IAPIResponseSuccess } from "@/types";
import { format } from "date-fns";
import { z } from "zod";
import {
  SelectionPlanCreateNewForm_PayloadSchema,
  SelectionPlan_APISuccessResponse,
} from "./schemas";

export interface ConfigProduct {
  config_product_id: number;
  config_product_code: string;
  config_product_label: string;
}

export interface ConfigProductVariationStateDetail {
  config_product_variation_state_id: number;
  config_product_variation_id: number;
  config_product_variation_code: string;
  config_product_variation_label: string;
  situs_state_id: number;
  state_name: string;
  state_code: string;
}

export interface RefState {
  state_id: number;
  state_name: string;
  state_code: string;
}

export const getProducts = async (): Promise<
  IAPIResponseSuccess<ConfigProduct[]>
> => {
  const res = await fetch("/api/config/products");
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  return res.json();
};

export const getProductVariationStates = async (
  config_product_id: number | undefined,
  selection_plan_effective_date: string | Date | undefined
): Promise<IAPIResponseSuccess<ConfigProductVariationStateDetail[]>> => {
  if (config_product_id == null) {
    throw new Error("config_product_id is required");
  }
  if (selection_plan_effective_date == null) {
    throw new Error("selection_plan_effective_date is required");
  }
  if (typeof selection_plan_effective_date === "object") {
    selection_plan_effective_date = format(
      selection_plan_effective_date,
      "yyyy-MM-dd"
    );
  }
  const res = await fetch(
    `/api/dd/product_variation_states?pid=${config_product_id}&dt=${selection_plan_effective_date}`
  );
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  return res.json();
};

export const getStates = async (): Promise<IAPIResponseSuccess<RefState[]>> => {
  const res = await fetch("/api/ref/states");
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  return res.json();
};

export const createDefaultPlan = async (
  input_data: z.infer<typeof SelectionPlanCreateNewForm_PayloadSchema>
) => {
  const res = await fetch("/rpc/selection/plan/create:plan-default", {
    method: "POST",
    body: JSON.stringify(input_data),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) {
    const err_data = await res.json();
    throw new Error(err_data.msg);
  }
  const data = await res.json();
  return SelectionPlan_APISuccessResponse.parseAsync(data);
};
