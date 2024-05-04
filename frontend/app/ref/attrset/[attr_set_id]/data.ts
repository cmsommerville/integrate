import * as api from "@/api-fetcher";
import { ConfigAttributeDetail } from "@/ref/types";

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

export const deleteConfigAttributeDetail = async (
  data: ConfigAttributeDetail
) => {
  return await api.DELETE(
    `/api/config/attribute/set/${data.config_attr_set_id}/detail/${data.config_attr_detail_id}`,
    {
      cache: "no-store",
    }
  );
};
