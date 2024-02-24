import * as z from "zod";
import * as api from "@/api-fetcher";
import { ProductVariationType } from "@/config/types";
import { ProductVariationFormSchema } from "./schemas";

export const getSingleVariation = async (id: number, product_id: number) => {
  const res = await api.GET(
    `/api/config/product/${product_id}/variation/${id}`,
    { cache: "no-cache" }
  );
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const createNewVariation = async (
  data: z.infer<typeof ProductVariationFormSchema>
) => {
  const output = ProductVariationFormSchema.safeParse(data);
  console.log("In createNewProduct");
  console.log(output);
};

export const updateExistingProduct = async (
  form_data: z.infer<typeof ProductVariationFormSchema>,
  previous_data: ProductVariationType
) => {
  const validated_output = ProductVariationFormSchema.safeParse(form_data);
  if (validated_output.success) {
    const { data: validated_data } = validated_output;
    const changed_data = Object.fromEntries(
      Object.entries(validated_data).filter(([k, val]) => {
        const key = k as keyof ProductVariationType;
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
