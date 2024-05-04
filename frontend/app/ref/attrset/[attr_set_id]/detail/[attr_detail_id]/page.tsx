import AppCard from "@/components/ui/AppCard";
import AppCardTitle from "@/components/ui/AppCardTitle";
import { getConfigAttributeDetail } from "./data";
import ConfigAttributeDetailDisplay from "./client";

export default async function ConfigAttributeDetailPage({
  params,
}: {
  params: { attr_set_id: string; attr_detail_id: string };
}) {
  const data = await getConfigAttributeDetail(
    params.attr_set_id,
    params.attr_detail_id
  );

  return (
    <AppCard className="max-w-fit">
      <AppCardTitle>Attribute Detail</AppCardTitle>
      <ConfigAttributeDetailDisplay data={data} />
    </AppCard>
  );
}
