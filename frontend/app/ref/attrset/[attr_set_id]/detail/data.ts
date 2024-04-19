import * as z from "zod";
import * as api from "@/api-fetcher";
import { ConfigAttributeDetail, NewConfigAttributeDetail } from "@/ref/types";
import { AttrDetailFormSchema } from "@/ref/schemas";

export const INITIAL_DATA: NewConfigAttributeDetail = {
  config_attr_set_id: -99,
  config_attr_detail_code: "",
  config_attr_detail_label: "",
};

export const getAttributeDetail = async (id: number) => {
  const res = await api.GET(`/api/config/attribute/set/${id}`, {
    cache: "no-cache",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const createNewAttributeDetail = async (
  data: z.infer<typeof AttrDetailFormSchema>
) => {
  const output = AttrDetailFormSchema.safeParse(data);
  if (output.success) {
    const res = await api.POST(
      `/api/config/attribute/set/${output.data.config_attr_set_id}/detail`,
      {
        body: JSON.stringify(output.data),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (res.ok) {
      const data = await res.json();
      return data;
    }
    throw new Error(res.statusText);
  }
};

export const updateExistingAttributeDetail = async (
  form_data: z.infer<typeof AttrDetailFormSchema>,
  previous_data: ConfigAttributeDetail
) => {
  const validated_output = AttrDetailFormSchema.safeParse(form_data);
  if (validated_output.success) {
    const { data: validated_data } = validated_output;
    const changed_data = Object.fromEntries(
      Object.entries(validated_data).filter(([k, val]) => {
        const key = k as keyof ConfigAttributeDetail;
        return val !== previous_data[key];
      })
    );
    console.log("In updateExistingAttributeSet");
    console.log({
      ...changed_data,
      config_attr_detail_id: previous_data.config_attr_detail_id,
    });
  }
};
