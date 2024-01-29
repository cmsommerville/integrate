"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_attr_detail_code",
    headerName: "Attr Code",
  },
  {
    field: "config_attr_detail_label",
    headerName: "Attr Label",
  },
];

export default function ClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Attribute Set"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select an attribute to edit or create a new one from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
