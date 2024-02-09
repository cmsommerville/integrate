import * as api from "@/api-fetcher";
import { ConfigAttributeSet } from "@/ref/types";

export const getConfigAttributeSets = async () => {
  const res = await api.GET("/api/config/attribute/sets", {
    cache: "no-store",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const deleteConfigAttributeSet = async (data: ConfigAttributeSet) => {
  return await api.DELETE(
    `/api/config/attribute/set/${data.config_attr_set_id}`,
    {
      cache: "no-store",
    }
  );
};
