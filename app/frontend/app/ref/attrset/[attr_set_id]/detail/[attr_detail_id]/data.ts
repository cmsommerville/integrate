import * as api from "@/api-fetcher";

export const getConfigAttributeDetail = async (
  set_id: string,
  detail_id: string
) => {
  const res = await api.GET(
    `/api/config/attribute/set/${set_id}/detail/${detail_id}`,
    {
      cache: "no-store",
    }
  );
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
