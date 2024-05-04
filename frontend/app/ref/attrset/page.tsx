import AppCard from "@/components/ui/AppCard";
import NewForm from "./NewForm";
import { INITIAL_DATA } from "./data";
import { ConfigAttributeSet } from "@/ref/types";

export default function NewAttributeSetPage() {
  return (
    <div className="flex items-start space-x-8">
      <AppCard className="w-2/3">
        <div className="space-y-4">
          <h2 className="text-lg">Create a new attribute set</h2>
          <hr />
          <NewForm data={INITIAL_DATA} />
        </div>
      </AppCard>
    </div>
  );
}
