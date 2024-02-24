import { RatingMapperCollectionTypeWithSetList } from "@/config/types";
import ClientGrid from "./client";
import { getRatingMapperCollection } from "./data";

export default async function RatingMapperCollection({
  params,
}: {
  params: { collection_id: string };
}) {
  const collection_data: RatingMapperCollectionTypeWithSetList =
    await getRatingMapperCollection(params.collection_id);

  const editHandler = async (row: any) => {
    "use server";
    return `/config/mappers/collection/${row.config_rating_mapper_collection_id}/set/${row.config_rating_mapper_set_id}`;
  };

  const newHandler = async () => {
    "use server";
    return `/config/mappers/collection/${params.collection_id}/set`;
  };

  return (
    <ClientGrid
      className="max-w-4xl"
      title="Rating Mappers"
      rowData={collection_data.mapper_sets}
      routes={{
        edit: editHandler,
        new: newHandler,
      }}
    />
  );
}
