import ClientGrid from "./client";
import { getRatingMapperCollections } from "./data";

export default async function RatingMapperCollection() {
  const row_data = await getRatingMapperCollections();
  console.log(row_data);

  const onEditHandler = async (row: any) => {
    "use server";
    return `/config/mappers/collection/${row.config_rating_mapper_collection_id}/`;
  };

  const newProductHandler = async () => {
    "use server";
    return `/config/mappers/collection`;
  };

  return (
    <ClientGrid
      className="max-w-4xl"
      title="Products"
      rowData={row_data}
      routes={{
        edit: onEditHandler,
        new: newProductHandler,
      }}
    />
  );
}
