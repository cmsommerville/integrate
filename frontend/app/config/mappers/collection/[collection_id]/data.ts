import * as api from "@/api-fetcher";

export const getRatingMapperCollection = async (collection_id: string) => {
  const res = await api.GET(`/api/config/mappers/collection/${collection_id}`, {
    cache: "no-store",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
