import ClientGrid from "./client";
import { getConfigAttributeDetails } from "./data";

export default async function ConfigAttributeSetLandingPage({
  params,
}: {
  params: { attr_set_id: string };
}) {
  const row_data = await getConfigAttributeDetails(params.attr_set_id);
  console.log(row_data);

  const editHandler = async (row: any) => {
    "use server";
    if (row.config_attr_detail_id) {
      return `/ref/attrset/${params.attr_set_id}/detail/${row.config_attr_detail_id}`;
    }
    return "";
  };

  const newHandler = async () => {
    "use server";
    return `/ref/attrset/${params.attr_set_id}/detail`;
  };

  return (
    <ClientGrid
      className="max-w-4xl"
      title="Attribute Details"
      rowData={row_data}
      routes={{
        edit: editHandler,
        new: newHandler,
      }}
    />
  );
}
