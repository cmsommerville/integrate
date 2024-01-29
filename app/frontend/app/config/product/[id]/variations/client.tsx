"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "ref_product_variation.ref_attr_label",
    headerName: "Product Variation",
  },
];

export default function ProductVariationsLandingClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Product Variations"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select a product variation to edit or create a new one from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
