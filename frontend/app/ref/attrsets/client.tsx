"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";
import DeleteRecord from "@/components/grid/DeleteRecord";
import { deleteConfigAttributeSet } from "./data";
import { ConfigAttributeSet } from "@/ref/types";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_attr_set_label",
    headerName: "Attribute",
  },
  {
    cellRenderer: DeleteRecord,
    cellRendererParams: {
      deleteMessage:
        "Do you want to delete? This will delete any attributes configured under this set.",
      onDelete: async (data: ConfigAttributeSet) => {
        return await deleteConfigAttributeSet(data);
      },
    },
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
