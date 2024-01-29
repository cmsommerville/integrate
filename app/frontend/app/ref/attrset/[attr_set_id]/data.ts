import * as api from "@/api-fetcher";

export const getConfigAttributeDetails = async (id: string) => {
  const res = await api.GET(`/api/config/attribute/set/${id}/details`, {
    cache: "no-store",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
