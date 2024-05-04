import AppCard from "@/components/ui/AppCard";
import NewForm from "./NewForm";
import { INITIAL_DATA } from "./data";

export default function NewAttributeSetPage({
  params,
}: {
  params: { attr_set_id: string };
}) {
  return (
    <div className="flex items-start space-x-8">
      <AppCard className="w-2/3">
        <div className="space-y-4">
          <h2 className="text-lg">Create a new attribute set</h2>
          <hr />
          <NewForm
            data={{
              ...INITIAL_DATA,
              config_attr_set_id: parseInt(params.attr_set_id),
            }}
            success_route={`/ref/attrset/${params.attr_set_id}`}
          />
        </div>
      </AppCard>
    </div>
  );
}
