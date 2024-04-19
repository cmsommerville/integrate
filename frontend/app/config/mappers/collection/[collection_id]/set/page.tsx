import ClientGrid from "./client";
import { getRatingMapperSets } from "./data";

export default async function RatingMapperSets({
  params,
}: {
  params: { collection_id: string };
}) {
  const row_data = await getRatingMapperSets(params.collection_id);

  const editHandler = async (row: any) => {
    "use server";
    return `/config/mappers/collection/${params.collection_id}/set/${row.config_product_mapper_set_id}/`;
  };

  const newHandler = async () => {
    "use server";
    return `/config/mappers/collection/${params.collection_id}/set`;
  };

  return (
    <ClientGrid
      className="max-w-4xl"
      title="Products"
      rowData={row_data}
      routes={{
        edit: editHandler,
        new: newHandler,
      }}
    />
  );
}
