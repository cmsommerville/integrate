import { getConfigAttributeDetail } from "@/ref/attrset/[attr_set_id]/detail/[attr_detail_id]/data";
import ViewConfigAttributeDetailModalClient from "./client";

export default async function ViewConfigAttributeDetailModal({
  params,
}: {
  params: { attr_set_id: string; attr_detail_id: string };
}) {
  const data = await getConfigAttributeDetail(
    params.attr_set_id,
    params.attr_detail_id
  );
  return <ViewConfigAttributeDetailModalClient data={data} />;
}
