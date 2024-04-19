import AppCard from "@/components/ui/AppCard";
import NewForm from "./NewForm";
import { INITIAL_DATA } from "./data";
import { getNewCollectionDropdowns } from "./data";

export default async function NewRatingMapperCollectionPage() {
  const dropdowns = await getNewCollectionDropdowns();

  return (
    <div className="flex items-start space-x-8">
      <AppCard className="w-2/3">
        <div className="space-y-4">
          <h2 className="text-lg">Create a new collection</h2>
          <hr />
          <NewForm collection={INITIAL_DATA} dropdowns={dropdowns} />
        </div>
      </AppCard>
    </div>
  );
}
