import * as api from "@/api-fetcher";
import { ConfigAttributeDetail } from "@/ref/types";

export const getConfigAttributeDetail = async (
  set_id: string,
  detail_id: string
): Promise<ConfigAttributeDetail> => {
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

export const editConfigAttributeDetail = async (
  data: ConfigAttributeDetail
) => {
  console.log("in EditConfigAttributeDetail");
  const res = await api.PUT(
    `/api/config/attribute/set/${data.config_attr_set_id}/detail/${data.config_attr_detail_id}`,
    {
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-store",
    }
  );
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};
