"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_attr_set_label",
    headerName: "Attribute",
  },
];

export default function ClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Attribute Sets"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select an attribute set to edit or create a new one from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
