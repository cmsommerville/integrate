"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";
import DeleteRecord from "@/components/grid/DeleteRecord";
import { deleteConfigAttributeDetail } from "./data";
import { ConfigAttributeDetail } from "@/ref/types";

const COL_DEFS: ColDef[] = [
  {
    field: "config_attr_detail_code",
    headerName: "Attr Code",
  },
  {
    field: "config_attr_detail_label",
    headerName: "Attr Label",
  },
  {
    cellRenderer: DeleteRecord,
    cellRendererParams: {
      onDelete: async (data: ConfigAttributeDetail) => {
        return await deleteConfigAttributeDetail(data);
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
      title="Attributes"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select an attribute to edit or add a new one!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
