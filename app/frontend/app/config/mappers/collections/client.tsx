"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_rating_mapper_collection_label",
    headerName: "Collection Name",
  },
  {
    field: "default_config_rating_mapper_set_id",
    headerName: "Default",
  },
];

export default function ClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Rating Mapper Collection"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select a collection to edit or create a new one from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
