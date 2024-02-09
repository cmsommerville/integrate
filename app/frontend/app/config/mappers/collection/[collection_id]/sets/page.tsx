import ClientGrid from "./client";
import { getRatingMapperSets } from "./data";

export default async function RatingMapperSets({
  params,
}: {
  params: { id: string };
}) {
  const row_data = await getRatingMapperSets(params.id);

  const editHandler = async (row: any) => {
    "use server";
    return `/config/mappers/collection/${params.id}/set/${row.config_product_mapper_set_id}/`;
  };

  const newHandler = async () => {
    "use server";
    return `/config/mappers/collection/${params.id}/set`;
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
