import * as api from "@/api-fetcher";

export const getProducts = async () => {
  const res = await api.GET("/api/config/products", {
    cache: "no-store",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
