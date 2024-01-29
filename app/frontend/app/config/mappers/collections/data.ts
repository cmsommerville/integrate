import * as api from "@/api-fetcher";

export const getRatingMapperCollections = async () => {
  const res = await api.GET("/api/config/mappers/collections", {
    cache: "no-store",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
