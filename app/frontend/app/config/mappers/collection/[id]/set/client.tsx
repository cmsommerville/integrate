"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_rating_mapper_set_label",
    headerName: "Mapper Name",
  },
  {
    field: "is_composite",
    headerName: "Composite",
  },
  {
    field: "is_employer_paid",
    headerName: "Employer Paid",
  },
];

export default function ClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Rating Mapper Set"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select a mapper to edit or create a new one from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
