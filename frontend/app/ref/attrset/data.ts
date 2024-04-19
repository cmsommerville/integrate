import * as z from "zod";
import * as api from "@/api-fetcher";
import { ConfigAttributeSet, NewConfigAttributeSet } from "../types";
import { AttrSetFormSchema } from "./schemas";

export const INITIAL_DATA: NewConfigAttributeSet = {
  config_attr_set_code: "",
  config_attr_set_label: "",
};

export const getAttributeSet = async (id: number) => {
  const res = await api.GET(`/api/config/attribute/set/${id}`, {
    cache: "no-cache",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const createNewAttributeSet = async (
  data: z.infer<typeof AttrSetFormSchema>
) => {
  const output = AttrSetFormSchema.safeParse(data);
  if (output.success) {
    const res = await api.POST(`/api/config/attribute/set`, {
      body: JSON.stringify(output.data),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      const data = await res.json();
      return data;
    }
    throw new Error(res.statusText);
  }
};

export const updateExistingAttributeSet = async (
  form_data: z.infer<typeof AttrSetFormSchema>,
  previous_data: ConfigAttributeSet
) => {
  const validated_output = AttrSetFormSchema.safeParse(form_data);
  if (validated_output.success) {
    const { data: validated_data } = validated_output;
    const changed_data = Object.fromEntries(
      Object.entries(validated_data).filter(([k, val]) => {
        const key = k as keyof ConfigAttributeSet;
        return val !== previous_data[key];
      })
    );
    console.log("In updateExistingAttributeSet");
    console.log({
      ...changed_data,
      config_attr_set_id: previous_data.config_attr_set_id,
    });
  }
};
