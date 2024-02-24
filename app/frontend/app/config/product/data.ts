import * as z from "zod";
import * as api from "@/api-fetcher";
import { ProductType } from "../types";
import { ProductFormSchema } from "./schemas";

export const getSingleProduct = async (id: number) => {
  const res = await api.GET(`/api/config/product/${id}`, { cache: "no-cache" });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const createNewProduct = async (
  data: z.infer<typeof ProductFormSchema>
) => {
  const output = ProductFormSchema.safeParse(data);
  console.log("In createNewProduct");
  console.log(output);
};

export const updateExistingProduct = async (
  form_data: z.infer<typeof ProductFormSchema>,
  previous_data: ProductType
) => {
  const validated_output = ProductFormSchema.safeParse(form_data);
  if (validated_output.success) {
    const { data: validated_data } = validated_output;
    const changed_data = Object.fromEntries(
      Object.entries(validated_data).filter(([k, val]) => {
        const key = k as keyof ProductType;
        return val !== previous_data[key];
      })
    );
    console.log("In updateExistingProduct");
    console.log({
      ...changed_data,
      config_product_id: previous_data.config_product_id,
    });
  }
};
