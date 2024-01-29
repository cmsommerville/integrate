import ClientGrid from "./client";
import { getConfigAttributeSets } from "./data";

export default async function ConfigAttributeSetsLandingPage() {
  const row_data = await getConfigAttributeSets();

  const editHandler = async (row: any) => {
    "use server";
    return `/ref/attrset/${row.config_attr_set_id}/`;
  };

  const newHandler = async () => {
    "use server";
    return `/ref/attrset/`;
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
