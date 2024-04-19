import * as api from "@/api-fetcher";

export const getVariations = async (product_id: number) => {
  const res = await api.GET(`/api/config/product/${product_id}/variations`);
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
